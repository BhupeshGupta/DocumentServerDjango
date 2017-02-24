# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    parentid = models.CharField(max_length=255, blank=True, null=True)
    parenttype = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    transactionid = models.CharField(db_column='transactionId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'


class Audittrail(models.Model):
    cno = models.CharField(max_length=255, blank=True, null=True)
    doctype = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    uploadedby = models.CharField(max_length=255, blank=True, null=True)
    uploadedon = models.DateTimeField(blank=True, null=True)
    verifiedby = models.CharField(max_length=255, blank=True, null=True)
    verifiedon = models.DateTimeField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    transactionid = models.CharField(db_column='transactionId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audittrail'


class Cheque(models.Model):
    chequedate = models.DateField(db_column='chequeDate', blank=True, null=True)  # Field name made lowercase.
    receivingdate = models.DateField(db_column='receivingDate', blank=True, null=True)  # Field name made lowercase.
    bankofcheque = models.CharField(db_column='bankOfCheque', max_length=255, blank=True, null=True)  # Field name made lowercase.
    chequenumber = models.CharField(db_column='chequeNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    customeraccount = models.CharField(db_column='customerAccount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(blank=True, null=True)
    chequeimage = models.IntegerField(db_column='chequeImage', unique=True, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(max_length=255, blank=True, null=True)
    payinslip = models.IntegerField(db_column='PayInSlip', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    transactionid = models.CharField(db_column='transactionId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cheque'


class ChequeChequesChequePayinslipCheques(models.Model):
    payinslip_cheques = models.IntegerField(blank=True, null=True)
    cheque_cheques_cheque = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cheque_cheques_cheque__payinslip_cheques'


class Payinslip(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    bankaccount = models.CharField(db_column='bankAccount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    transactionid = models.CharField(db_column='transactionId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payinslip'


class Photoofcheque(models.Model):
    fd = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'photoofcheque'



