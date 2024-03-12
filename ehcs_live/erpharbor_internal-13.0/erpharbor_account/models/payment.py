# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    charges_amount = fields.Monetary(string='Charges', states={'draft': [('readonly', False)]}, tracking=True)
    gst_tax_amount = fields.Float('GST Amount', digits='GST Tax Amount')
    currency_rate = fields.Float('Currency Rate (INR)', digits='Inv Currency Rate')

    @api.onchange('charges_amount', 'journal_id')
    def onchange_charges_amount(self):
        res = self._onchange_journal()
        self.amount -= self.charges_amount
        if self.charges_amount > 0:
            self.payment_difference_handling = 'reconcile'
            self.writeoff_label = 'Bank Charges'
            self.writeoff_account_id = self.journal_id.charges_account_id.id
        return res

#    def _prepare_payment_moves(self):
#        """Override to pass the GST entry to payment journal entry"""
#        all_move_vals = super(AccountPayment, self.with_context(currency_rate=self.currency_rate))._prepare_payment_moves()
#        for payment in self.filtered(
#            lambda p: p.payment_type == 'inbound' and p.gst_tax_amount > 0
#        ):
#            # Skip if Company and Invoice Currency are same
#            if payment.currency_id == payment.company_id.currency_id:
#                continue
#            gst_tax_amt = payment.gst_tax_amount
#            gst_account_id = payment.company_id.gst_account_id.id
#            if not gst_account_id:
#                raise ValidationError(_("Please configure GST Account in Company."))
#            gst_line = []
#            for move_vals in all_move_vals:
#                for line_tpl in move_vals.get('line_ids', []):
#                    line_vals = line_tpl[2]
#                    if (
#                        line_vals['account_id'] == payment.journal_id.default_credit_account_id.id and
#                        line_vals['payment_id'] == payment.id
#                    ):
#                        line_vals['debit'] -= gst_tax_amt
#                        gst_line.append((0, 0, {
#                            'name': 'FCC-GST',
#                            'debit': gst_tax_amt or 0.0,
#                            'credit': 0.0,
#                            'date_maturity': payment.payment_date,
#                            'partner_id': payment.partner_id.commercial_partner_id.id,
#                            'account_id': gst_account_id,
#                            'payment_id': payment.id,
#                        }))
#                if gst_line:
#                    move_vals['line_ids'].extend(gst_line)
#        return all_move_vals

    def _prepare_payment_moves(self):
        '''Overwrite to pass the GST Entries and keep invoice open for
            partial payment and pass the Bank Charges using write-off feature
        '''
        # Pass Currency Rate
        self = self.with_context(currency_rate=self.currency_rate)
        all_move_vals = []
        for payment in self:
            company_currency = payment.company_id.currency_id
            move_names = payment.move_name.split(payment._get_move_name_transfer_separator()) if payment.move_name else None

# CUSTOMIZATION START: FOR PARTIAL PAYMENT
            # Compute amounts.
#            write_off_amount = payment.payment_difference_handling == 'reconcile' and -payment.payment_difference or 0.0
            write_off_amount = 0
            if payment.payment_difference_handling == 'reconcile':
                write_off_amount = -payment.payment_difference or 0.0
            elif payment.payment_difference_handling == 'open':
                write_off_amount = -payment.charges_amount or 0.0
# CUSTOMIZATION END

            if payment.payment_type in ('outbound', 'transfer'):
                counterpart_amount = payment.amount
                liquidity_line_account = payment.journal_id.default_debit_account_id
            else:
                counterpart_amount = -payment.amount
                liquidity_line_account = payment.journal_id.default_credit_account_id

            # Manage currency.
            if payment.currency_id == company_currency:
                # Single-currency.
                balance = counterpart_amount
                write_off_balance = write_off_amount
                counterpart_amount = write_off_amount = 0.0
                currency_id = False
            else:
                # Multi-currencies.
                balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id, payment.payment_date)
                write_off_balance = payment.currency_id._convert(write_off_amount, company_currency, payment.company_id, payment.payment_date)
                currency_id = payment.currency_id.id

            # Manage custom currency on journal for liquidity line.
            if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                # Custom currency on journal.
                if payment.journal_id.currency_id == company_currency:
                    # Single-currency
                    liquidity_line_currency_id = False
                else:
                    liquidity_line_currency_id = payment.journal_id.currency_id.id
                liquidity_amount = company_currency._convert(
                    balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date)
            else:
                # Use the payment currency.
                liquidity_line_currency_id = currency_id
                liquidity_amount = counterpart_amount

            # Compute 'name' to be used in receivable/payable line.
            rec_pay_line_name = ''
            if payment.payment_type == 'transfer':
                rec_pay_line_name = payment.name
            else:
                if payment.partner_type == 'customer':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Customer Payment")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Customer Credit Note")
                elif payment.partner_type == 'supplier':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Vendor Credit Note")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Vendor Payment")
                if payment.invoice_ids:
                    rec_pay_line_name += ': %s' % ', '.join(payment.invoice_ids.mapped('name'))

            # Compute 'name' to be used in liquidity line.
            if payment.payment_type == 'transfer':
                liquidity_line_name = _('Transfer to %s') % payment.destination_journal_id.name
            else:
                liquidity_line_name = payment.name

            # ==== 'inbound' / 'outbound' ====

            move_vals = {
                'date': payment.payment_date,
                'ref': payment.communication,
                'journal_id': payment.journal_id.id,
                'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                'partner_id': payment.partner_id.id,
                'line_ids': [
                    # Receivable / Payable / Transfer line.
                    (0, 0, {
                        'name': rec_pay_line_name,
                        'amount_currency': counterpart_amount + write_off_amount if currency_id else 0.0,
                        'currency_id': currency_id,
                        'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                        'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.commercial_partner_id.id,
                        'account_id': payment.destination_account_id.id,
                        'payment_id': payment.id,
                    }),
                    # Liquidity line.
                    (0, 0, {
                        'name': liquidity_line_name,
                        'amount_currency': -liquidity_amount if liquidity_line_currency_id else 0.0,
                        'currency_id': liquidity_line_currency_id,
                        'debit': balance < 0.0 and -balance or 0.0,
                        'credit': balance > 0.0 and balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.commercial_partner_id.id,
                        'account_id': liquidity_line_account.id,
                        'payment_id': payment.id,
                    }),
                ],
            }
            if write_off_balance:
                # Write-off line.
                move_vals['line_ids'].append((0, 0, {
                    'name': payment.writeoff_label,
                    'amount_currency': -write_off_amount,
                    'currency_id': currency_id,
                    'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                    'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment.writeoff_account_id.id,
                    'payment_id': payment.id,
                }))

            if move_names:
                move_vals['name'] = move_names[0]

            all_move_vals.append(move_vals)

            # ==== 'transfer' ====
            if payment.payment_type == 'transfer':
                journal = payment.destination_journal_id

                # Manage custom currency on journal for liquidity line.
                if journal.currency_id and payment.currency_id != journal.currency_id:
                    # Custom currency on journal.
                    liquidity_line_currency_id = journal.currency_id.id
                    transfer_amount = company_currency._convert(balance, journal.currency_id, payment.company_id, payment.payment_date)
                else:
                    # Use the payment currency.
                    liquidity_line_currency_id = currency_id
                    transfer_amount = counterpart_amount

                transfer_move_vals = {
                    'date': payment.payment_date,
                    'ref': payment.communication,
                    'partner_id': payment.partner_id.id,
                    'journal_id': payment.destination_journal_id.id,
                    'line_ids': [
                        # Transfer debit line.
                        (0, 0, {
                            'name': payment.name,
                            'amount_currency': -counterpart_amount if currency_id else 0.0,
                            'currency_id': currency_id,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': payment.company_id.transfer_account_id.id,
                            'payment_id': payment.id,
                        }),
                        # Liquidity credit line.
                        (0, 0, {
                            'name': _('Transfer from %s') % payment.journal_id.name,
                            'amount_currency': transfer_amount if liquidity_line_currency_id else 0.0,
                            'currency_id': liquidity_line_currency_id,
                            'debit': balance > 0.0 and balance or 0.0,
                            'credit': balance < 0.0 and -balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': payment.destination_journal_id.default_credit_account_id.id,
                            'payment_id': payment.id,
                        }),
                    ],
                }

                if move_names and len(move_names) == 2:
                    transfer_move_vals['name'] = move_names[1]

                all_move_vals.append(transfer_move_vals)

# CUSTOMIZATION START
            # Pass the GST entry to payment journal entry
            if payment.payment_type == 'inbound' and payment.gst_tax_amount > 0:
                # Skip if Company and Invoice Currency are same
                if payment.currency_id == payment.company_id.currency_id:
                    continue
                gst_tax_amt = payment.gst_tax_amount
                gst_account_id = payment.company_id.gst_account_id.id
                if not gst_account_id:
                    raise ValidationError(_("Please configure GST Account in Company."))
                gst_line = []
                for move_vals in all_move_vals:
                    for line_tpl in move_vals.get('line_ids', []):
                        line_vals = line_tpl[2]
                        if (
                            line_vals['account_id'] == payment.journal_id.default_credit_account_id.id and
                            line_vals['payment_id'] == payment.id
                        ):
                            line_vals['debit'] -= gst_tax_amt
                            gst_line.append((0, 0, {
                                'name': 'FCC-GST',
                                'debit': gst_tax_amt or 0.0,
                                'credit': 0.0,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.commercial_partner_id.id,
                                'account_id': gst_account_id,
                                'payment_id': payment.id,
                            }))
                    if gst_line:
                        move_vals['line_ids'].extend(gst_line)
# CUSTOMIZATION END

        return all_move_vals
