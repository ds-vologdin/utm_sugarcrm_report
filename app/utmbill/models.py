import logging
from sqlalchemy import Column, Float, Index, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base

from .utm_db import Session_utm

Base = declarative_base()
metadata = Base.metadata
Base.query = Session_utm.query_property()


class BalanceHistory(Base):
    __tablename__ = 'balance_history'

    id = Column(Integer, primary_key=True, server_default=text("nextval('balance_history_id_seq'::regclass)"))
    account_id = Column(Integer, server_default=text("0"))
    accounting_period_id = Column(Integer, server_default=text("0"))
    out_balance = Column(Float)
    date = Column(Integer, server_default=text("0"))


class BlocksInfo(Base):
    __tablename__ = 'blocks_info'
    __table_args__ = (
        Index('first_block', 'start_date', 'expire_date', 'account_id', 'is_deleted', 'what_blocked'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('blocks_info_id_seq'::regclass)"))
    user_id = Column(Integer)
    account_id = Column(Integer)
    slink_id = Column(Integer)
    what_blocked = Column(Integer, server_default=text("0"))
    block_type = Column(Integer, server_default=text("0"))
    start_date = Column(Integer, server_default=text("0"))
    expire_date = Column(Integer, server_default=text("2000000000"))
    is_planning = Column(Integer, server_default=text("0"))
    is_deleted = Column(Integer, server_default=text("0"))
    service_id = Column(Integer)
    unabon = Column(Integer)
    unprepay = Column(Integer)
    comment = Column(String(255))


class PaymentTransaction(Base):
    __tablename__ = 'payment_transactions'
    __table_args__ = (
        Index('first_ptr', 'actual_date', 'account_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('payment_transactions_id_seq'::regclass)"))
    account_id = Column(Integer)
    payment_incurrency = Column(Float)
    currency_id = Column(Integer)
    currency_rate = Column(Float)
    payment_absolute = Column(Float)
    actual_date = Column(Integer)
    payment_enter_date = Column(Integer)
    payment_ext_number = Column(String(255), server_default=text("''::character varying"))
    method = Column(Integer)
    who_receive = Column(Integer)
    comments_for_user = Column(String(255))
    comments_for_admins = Column(String(255))
    burn_time = Column(Integer, server_default=text("0"))
    discount_transaction_id = Column(Integer, server_default=text("0"))
    dealer_transaction_id = Column(Integer, server_default=text("0"))
    dealer_client_account_id = Column(Integer, server_default=text("0"))
    is_canceled = Column(Integer, server_default=text("0"))
    cancel_id = Column(Integer, server_default=text("0"))
    hash = Column(String(255), index=True)
    charge_id = Column(Integer, nullable=False, server_default=text("0"))
    ic_status = Column(Integer, nullable=False, server_default=text("0"))


class ServiceLink(Base):
    __tablename__ = 'service_links'

    id = Column(Integer, primary_key=True, server_default=text("nextval('service_links_id_seq'::regclass)"))
    user_id = Column(Integer)
    account_id = Column(Integer)
    service_id = Column(Integer)
    tariff_link_id = Column(Integer)
    is_deleted = Column(Integer, server_default=text("0"))


class ServicesDatum(Base):
    __tablename__ = 'services_data'

    id = Column(Integer, primary_key=True, server_default=text("nextval('services_data_id_seq'::regclass)"))
    service_type = Column(Integer)
    service_name = Column(String(255))
    comment = Column(String(255))
    comission_value = Column(Float, server_default=text("(0)::real"))
    is_deleted = Column(Integer, server_default=text("0"))
    tariff_id = Column(Integer, server_default=text("0"))
    parent_service_id = Column(Integer, server_default=text("0"))
    default_dp_type = Column(Integer, server_default=text("0"))
    link_by_default = Column(Integer, server_default=text("0"))
    is_dynamic = Column(Integer, server_default=text("0"))


class TariffsHistory(Base):
    __tablename__ = 'tariffs_history'

    id = Column(Integer, primary_key=True, server_default=text("nextval('tariffs_history_id_seq'::regclass)"))
    account_id = Column(Integer, nullable=False, server_default=text("0"))
    tariff_id = Column(Integer, nullable=False, server_default=text("0"))
    link_date = Column(Integer, nullable=False, server_default=text("0"))
    unlink_date = Column(Integer, nullable=False, server_default=text("0"))
    tariff_name = Column(String(255), nullable=False, server_default=text("''::character varying"))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    login = Column(String(255), server_default=text("''::character varying"))
    password = Column(String(255), server_default=text("''::character varying"))
    basic_account = Column(Integer, server_default=text("0"))
    is_blocked = Column(Integer, server_default=text("0"))
    discount_period_id = Column(Integer, server_default=text("0"))
    advance_payment = Column(Integer, server_default=text("0"))
    create_date = Column(Integer)
    last_change_date = Column(Integer)
    who_create = Column(Integer)
    who_change = Column(Integer)
    is_juridical = Column(Integer, server_default=text("0"))
    full_name = Column(Text)
    juridical_address = Column(Text)
    actual_address = Column(Text)
    work_telephone = Column(String(255))
    home_telephone = Column(String(255))
    mobile_telephone = Column(String(255))
    web_page = Column(String(255))
    icq_number = Column(String(255))
    tax_number = Column(String(255))
    kpp_number = Column(String(255))
    bank_id = Column(Integer, server_default=text("0"))
    bank_account = Column(String(255))
    email = Column(String(255))
    house_id = Column(Integer)
    flat_number = Column(String(255))
    entrance = Column(String(255))
    floor = Column(String(255))
    district = Column(String(255))
    building = Column(String(255))
    passport = Column(String(255))
    comments = Column(Text)
    personal_manager = Column(String(255))
    connect_date = Column(Integer)
    remote_switch_id = Column(Integer, server_default=text("0"))
    port_number = Column(Integer, server_default=text("0"))
    personal_currency_coef = Column(Float, server_default=text("(1)::real"))
    binded_currency_code = Column(Integer, server_default=text("810"))
    is_deleted = Column(Integer, server_default=text("0"))
    is_send_invoice = Column(Integer, server_default=text("0"))
    ic_status = Column(Integer, nullable=False, server_default=text("0"))
