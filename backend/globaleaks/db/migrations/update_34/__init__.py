# -*- coding: utf-8 -*-
import base64
import os

from six import binary_type, text_type

from globaleaks import models
from globaleaks.db.migrations.update import MigrationBase
from globaleaks.db.migrations.update_34.config_desc import GLConfig_v_35
from globaleaks.models.properties import *
from globaleaks.settings import Settings
from globaleaks.utils.utility import datetime_null, iso_strf_time

class Node_v_33(models.Model):
    __tablename__ = 'node'
    id = Column(UnicodeText(36), primary_key=True, default=uuid4, nullable=False)
    version = Column(UnicodeText)
    version_db = Column(UnicodeText)
    name = Column(UnicodeText, default=u'')
    basic_auth = Column(Boolean, default=False)
    basic_auth_username = Column(UnicodeText, default=u'')
    basic_auth_password = Column(UnicodeText, default=u'')
    public_site = Column(UnicodeText, default=u'')
    hidden_service = Column(UnicodeText, default=u'')
    tb_download_link = Column(UnicodeText, default=u'https://www.torproject.org/download/download')
    receipt_salt = Column(UnicodeText)
    languages_enabled = Column(JSON)
    default_language = Column(UnicodeText, default=u'en')
    default_password = Column(UnicodeText, default=u'globaleaks')
    description = Column(JSON, default=dict)
    presentation = Column(JSON, default=dict)
    footer = Column(JSON, default=dict)
    security_awareness_title = Column(JSON, default=dict)
    security_awareness_text = Column(JSON, default=dict)
    maximum_namesize = Column(Integer, default=128)
    maximum_textsize = Column(Integer, default=4096)
    maximum_filesize = Column(Integer, default=30)
    tor2web_admin = Column(Boolean, default=True)
    tor2web_custodian = Column(Boolean, default=True)
    tor2web_whistleblower = Column(Boolean, default=False)
    tor2web_receiver = Column(Boolean, default=True)
    tor2web_unauth = Column(Boolean, default=True)
    allow_unencrypted = Column(Boolean, default=False)
    disable_encryption_warnings = Column(Boolean, default=False)
    allow_iframes_inclusion = Column(Boolean, default=False)
    submission_minimum_delay = Column(Integer, default=10)
    submission_maximum_ttl = Column(Integer, default=10800)
    can_postpone_expiration = Column(Boolean, default=False)
    can_delete_submission = Column(Boolean, default=False)
    can_grant_permissions = Column(Boolean, default=False)
    ahmia = Column(Boolean, default=False)
    allow_indexing = Column(Boolean, default=False)
    wizard_done = Column(Boolean, default=False)
    disable_submissions = Column(Boolean, default=False)
    disable_privacy_badge = Column(Boolean, default=False)
    disable_security_awareness_badge = Column(Boolean, default=False)
    disable_security_awareness_questions = Column(Boolean, default=False)
    disable_key_code_hint = Column(Boolean, default=False)
    disable_donation_panel = Column(Boolean, default=False)
    enable_captcha = Column(Boolean, default=True)
    enable_proof_of_work = Column(Boolean, default=True)
    enable_experimental_features = Column(Boolean, default=False)
    whistleblowing_question = Column(JSON, default=dict)
    whistleblowing_button = Column(JSON, default=dict)
    whistleblowing_receipt_prompt = Column(JSON, default=dict)
    simplified_login = Column(Boolean, default=True)
    enable_custom_privacy_badge = Column(Boolean, default=False)
    custom_privacy_badge_tor = Column(JSON, default=dict)
    custom_privacy_badge_none = Column(JSON, default=dict)
    header_title_homepage = Column(JSON, default=dict)
    header_title_submissionpage = Column(JSON, default=dict)
    header_title_receiptpage = Column(JSON, default=dict)
    header_title_tippage = Column(JSON, default=dict)
    widget_comments_title = Column(JSON, default=dict)
    widget_messages_title = Column(JSON, default=dict)
    widget_files_title = Column(JSON, default=dict)
    landing_page = Column(UnicodeText, default=u'homepage')
    contexts_clarification = Column(JSON, default=dict)
    show_small_context_cards = Column(Boolean, default=False)
    show_contexts_in_alphabetical_order = Column(Boolean, default=False)
    wbtip_timetolive = Column(Integer, default=90)
    threshold_free_disk_megabytes_high = Column(Integer, default=200)
    threshold_free_disk_megabytes_medium = Column(Integer, default=500)
    threshold_free_disk_megabytes_low = Column(Integer, default=1000)
    threshold_free_disk_percentage_high = Column(Integer, default=3)
    threshold_free_disk_percentage_medium = Column(Integer, default=5)
    threshold_free_disk_percentage_low = Column(Integer, default=10)
    context_selector_type = Column(UnicodeText, default=u'list')

    localized_keys = [
        'description',
        'presentation',
        'footer',
        'security_awareness_title',
        'security_awareness_text',
        'whistleblowing_question',
        'whistleblowing_button',
        'whistleblowing_receipt_prompt',
        'custom_privacy_badge_tor',
        'custom_privacy_badge_none',
        'header_title_homepage',
        'header_title_submissionpage',
        'header_title_receiptpage',
        'header_title_tippage',
        'contexts_clarification',
        'widget_comments_title',
        'widget_messages_title',
        'widget_files_title'
    ]


class Notification_v_33(models.Model):
    __tablename__ = 'notification'
    id = Column(UnicodeText(36), primary_key=True, default=uuid4, nullable=False)
    server = Column(UnicodeText, default=u'demo.globaleaks.org')
    port = Column(Integer, default=9267)
    username = Column(UnicodeText, default=u'hey_you_should_change_me')
    password = Column(UnicodeText, default=u'yes_you_really_should_change_me')
    source_name = Column(UnicodeText, default=u'GlobaLeaks - CHANGE EMAIL ACCOUNT USED FOR NOTIFICATION')
    source_email = Column(UnicodeText, default=u'notification@demo.globaleaks.org')
    security = Column(UnicodeText, default=u'TLS')
    admin_pgp_alert_mail_title = Column(JSON)
    admin_pgp_alert_mail_template = Column(JSON)
    admin_anomaly_mail_template = Column(JSON)
    admin_anomaly_mail_title = Column(JSON)
    admin_anomaly_disk_low = Column(JSON)
    admin_anomaly_disk_medium = Column(JSON)
    admin_anomaly_disk_high = Column(JSON)
    admin_anomaly_activities = Column(JSON)
    admin_test_static_mail_template = Column(JSON)
    admin_test_static_mail_title = Column(JSON)
    tip_mail_template = Column(JSON)
    tip_mail_title = Column(JSON)
    file_mail_template = Column(JSON)
    file_mail_title = Column(JSON)
    comment_mail_template = Column(JSON)
    comment_mail_title = Column(JSON)
    message_mail_template = Column(JSON)
    message_mail_title = Column(JSON)
    tip_expiration_mail_template = Column(JSON)
    tip_expiration_mail_title = Column(JSON)
    pgp_alert_mail_title = Column(JSON)
    pgp_alert_mail_template = Column(JSON)
    receiver_notification_limit_reached_mail_template = Column(JSON)
    receiver_notification_limit_reached_mail_title = Column(JSON)
    export_template = Column(JSON)
    export_message_recipient = Column(JSON)
    export_message_whistleblower = Column(JSON)
    identity_access_authorized_mail_template = Column(JSON)
    identity_access_authorized_mail_title = Column(JSON)
    identity_access_denied_mail_template = Column(JSON)
    identity_access_denied_mail_title = Column(JSON)
    identity_access_request_mail_template = Column(JSON)
    identity_access_request_mail_title = Column(JSON)
    identity_provided_mail_template = Column(JSON)
    identity_provided_mail_title = Column(JSON)
    disable_admin_notification_emails = Column(Boolean, default=False)
    disable_custodian_notification_emails = Column(Boolean, default=False)
    disable_receiver_notification_emails = Column(Boolean, default=False)
    send_email_for_every_event = Column(Boolean, default=True)
    tip_expiration_threshold = Column(Integer, default=72)
    notification_threshold_per_hour = Column(Integer, default=20)
    notification_suspension_time=Column(Integer, default=(2 * 3600))
    exception_email_address = Column(UnicodeText, default=u'globaleaks-stackexception@lists.globaleaks.org')
    exception_email_pgp_key_fingerprint = Column(UnicodeText, default=u'')
    exception_email_pgp_key_public = Column(UnicodeText, default=u'')
    exception_email_pgp_key_expiration = Column(DateTime, default=datetime_null)

    localized_keys = [
        'admin_anomaly_mail_title',
        'admin_anomaly_mail_template',
        'admin_anomaly_disk_low',
        'admin_anomaly_disk_medium',
        'admin_anomaly_disk_high',
        'admin_anomaly_activities',
        'admin_pgp_alert_mail_title',
        'admin_pgp_alert_mail_template',
        'admin_test_static_mail_template',
        'admin_test_static_mail_title',
        'pgp_alert_mail_title',
        'pgp_alert_mail_template',
        'tip_mail_template',
        'tip_mail_title',
        'file_mail_template',
        'file_mail_title',
        'comment_mail_template',
        'comment_mail_title',
        'message_mail_template',
        'message_mail_title',
        'tip_expiration_mail_template',
        'tip_expiration_mail_title',
        'receiver_notification_limit_reached_mail_template',
        'receiver_notification_limit_reached_mail_title',
        'identity_access_authorized_mail_template',
        'identity_access_authorized_mail_title',
        'identity_access_denied_mail_template',
        'identity_access_denied_mail_title',
        'identity_access_request_mail_template',
        'identity_access_request_mail_title',
        'identity_provided_mail_template',
        'identity_provided_mail_title',
        'export_template',
        'export_message_whistleblower',
        'export_message_recipient'
    ]


class MigrationScript(MigrationBase):
    def epilogue(self):
        old_node = self.session_old.query(self.model_from['Node']).one()
        old_notif = self.session_old.query(self.model_from['Notification']).one()

        with open(os.path.join(Settings.client_path, 'data', 'favicon.ico'), 'rb') as favicon_file:
            data = favicon_file.read()
            new_file = self.model_to['File']()
            new_file.id = u'favicon'
            new_file.data = base64.b64encode(data).decode()
            self.session_new.add(new_file)
            self.entries_count['File'] += 1

        file_path = os.path.join(Settings.files_path, 'custom_homepage.html')
        if os.path.exists(file_path):
            with open(file_path, 'r') as homepage_file:
                data = homepage_file.read()
                new_file = self.model_to['File']()
                new_file.id = u'homepage'
                new_file.data = base64.b64encode(data).decode()
                self.session_new.add(new_file)
                self.entries_count['File'] += 1

            os.remove(file_path)

        #### Create ConfigL10N table and rows ####
        for lang in old_node.languages_enabled:
            self.session_new.add(self.model_to['EnabledLanguage'](lang))

        self._migrate_l10n_static_config(old_node, 'node')
        self._migrate_l10n_static_config(old_notif, 'templates')

        # TODO assert that localized_keys matches exactly what is stored in the DB

        #### Create Config table and rows ####

        # Migrate Config saved in Node
        for var_name, _ in GLConfig_v_35['node'].items():
            old_val = getattr(old_node, var_name)
            self.session_new.add(self.model_to['Config']('node', var_name, old_val))

        # Migrate Config saved in Notification
        for var_name, _ in GLConfig_v_35['notification'].items():
            old_val = getattr(old_notif, var_name)

            if var_name == 'exception_email_pgp_key_expiration' and old_val is not None:
                old_val = iso_strf_time(old_val)

            self.session_new.add(self.model_to['Config']('notification', var_name, old_val))

        # Migrate private fields
        salt = old_node.receipt_salt
        if isinstance(old_node.receipt_salt, binary_type):
            salt = salt.decode()

        self.session_new.add(self.model_to['Config']('private', 'receipt_salt', salt))
        self.session_new.add(self.model_to['Config']('private', 'smtp_password', old_notif.password))

        # Set old verions that will be then handled by the version update
        self.session_new.add(self.model_to['Config']('private', 'version', 'X.Y.Z'))
        self.session_new.add(self.model_to['Config']('private', 'version_db', 0))

    def _migrate_l10n_static_config(self, old_obj, appd_key):
        langs_enabled = self.model_to['EnabledLanguage'].list(self.session_new)

        new_obj_appdata = self.appdata[appd_key]

        for name in old_obj.localized_keys:
            xx_json_dict = getattr(old_obj, name, {})
            if xx_json_dict is None:
                xx_json_dict = {} # protects against Nones in early db versions
            app_data_item = new_obj_appdata.get(name, {})
            for lang in langs_enabled:
                val = xx_json_dict.get(lang, None)
                val_def = app_data_item.get(lang, "")

                if val is not None:
                    val_f = val
                elif val is None and val_def != "":
                    # This is the reset of the new default
                    val_f = val_def
                else: # val is None and val_def == ""
                    val_f = ""

                s = self.model_to['ConfigL10N'](lang, old_obj.__tablename__, name, val_f)
                # Set the cfg item to customized if the final assigned val does
                # not equal the current default template value
                s.customized = val_f != val_def

                self.session_new.add(s)

    def migrate_Field(self):
        old_objs = self.session_old.query(self.model_from['Field'])
        for old_obj in old_objs:
            new_obj = self.model_to['Field']()
            for key in [c.key for c in new_obj.__table__.columns]:
                setattr(new_obj, key, getattr(old_obj, key))

            if (new_obj.instance == 'instance' and new_obj.step_id is None and new_obj.fieldgroup_id is None or
               new_obj.instance == 'reference' and new_obj.step_id is None and new_obj.fieldgroup_id is None or
               new_obj.instance == 'template' and not(new_obj.step_id is None or new_obj.fieldgroup_id is None)):

                # This fix is necessary in order to remove zombies caused by a step removal or a parent field removal
                # The issue was caused by the db reference deleting only the StepField/FieldField relations but not the childrens hierarchy
                # The issue affected al releases before database 28 and the fix is added here in order to remove the dead fields
                # that are still stored inside databases migrated from a version <28 up to the current version.
                self.entries_count['Field'] -= 1
                continue

            # Produce something of value

            self.session_new.add(new_obj)
