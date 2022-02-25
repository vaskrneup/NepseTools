from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare
from nepse_tools.utils.data_loader import load_test_data


class TestMeroshare:
    ms = MeroShare(
        dp=config("MEROSHARE_DP"),
        username=config("MEROSHARE_USERNAME"),
        password=config("MEROSHARE_PASSWORD"),
        pin=config("MEROSHARE_PIN"),
    )
    TEST_DATA = load_test_data("meroshare_test_data.json")

    def check_with_test_data(self, key, test_value):
        real_value = self.TEST_DATA.get(key, "#__BLANK__#")

        if real_value == "#__BLANK__#":
            return None
        else:
            assert real_value == test_value

    def test_login(self) -> None:
        login_data = self.ms.login()

        self.check_with_test_data(key="login", test_value=login_data)
        assert login_data is not None, "Login Unsuccessful"

    def test_load_client_id_data(self) -> None:
        load_client_id_data = self.ms.load_client_id_data()

        self.check_with_test_data(key="load_client_id_data", test_value=load_client_id_data)
        assert load_client_id_data is not None

    def test_load_initial_data__own_data(self) -> None:
        own_data = self.ms.load_initial_data__own_data()

        self.check_with_test_data(key="load_initial_data__own_data", test_value=own_data)
        assert own_data is not None

    def test_load_bank_details__my_details(self) -> None:
        my_details = self.ms.load_bank_details__my_details()

        self.check_with_test_data(key="load_bank_details__my_details", test_value=my_details)
        assert my_details is not None

    def test_load_bank_request(self) -> None:
        bank_request = self.ms.load_bank_request()

        self.check_with_test_data(key="load_bank_request", test_value=bank_request)
        assert bank_request is not None

    def test_bank_branch(self) -> None:
        self.check_with_test_data(key="bank_branch", test_value=self.ms.bank_branch)
        assert type(self.ms.bank_branch) is str

    def test_bank_branch_code(self) -> None:
        self.check_with_test_data(key="bank_branch_code", test_value=self.ms.bank_branch_code)
        assert type(self.ms.bank_branch_code) is str

    def test_bank_branch_id(self) -> None:
        self.check_with_test_data(key="bank_branch_id", test_value=self.ms.bank_branch_id)
        assert type(self.ms.bank_branch_id) is int

    def test_bank_id(self) -> None:
        self.check_with_test_data(key="bank_id", test_value=self.ms.bank_id)
        assert type(self.ms.bank_id) is int

    def test_capital_code(self) -> None:
        self.check_with_test_data(key="capital_code", test_value=self.ms.capital_code)
        assert type(self.ms.capital_code) is str

    def test_capital_id(self) -> None:
        self.check_with_test_data(key="capital_id", test_value=self.ms.capital_id)
        assert type(self.ms.capital_id) is int

    def test_capital_name(self) -> None:
        self.check_with_test_data(key="capital_name", test_value=self.ms.capital_name)
        assert type(self.ms.capital_name) is str

    def test_account_creation_detail(self) -> None:
        self.check_with_test_data(key="account_creation_detail", test_value=self.ms.account_creation_detail)
        assert type(self.ms.account_creation_detail) is dict

    def test_crn_number(self) -> None:
        self.check_with_test_data(key="crn_number", test_value=self.ms.crn_number)
        assert type(self.ms.crn_number) is str

    def test_kyc_detail(self) -> None:
        self.check_with_test_data(key="kyc_detail", test_value=self.ms.kyc_detail)
        assert type(self.ms.kyc_detail) is dict

    def test_account_number(self) -> None:
        self.check_with_test_data(key="account_number", test_value=self.ms.account_number)
        assert type(self.ms.account_number) is str

    def test_account_open_date(self) -> None:
        self.check_with_test_data(key="account_open_date", test_value=self.ms.account_open_date)
        assert type(self.ms.account_open_date) is str

    def test_account_status(self) -> None:
        self.check_with_test_data(key="account_status", test_value=self.ms.account_status)
        assert type(self.ms.account_status) is int

    def test_account_status_flag(self) -> None:
        self.check_with_test_data(key="account_status_flag", test_value=self.ms.account_status_flag)
        assert type(self.ms.account_status_flag) is str

    def test_account_status_name(self) -> None:
        self.check_with_test_data(key="account_status_name", test_value=self.ms.account_status_name)
        assert type(self.ms.account_status_name) is str

    def test_account_type(self) -> None:
        self.check_with_test_data(key="account_type", test_value=self.ms.account_type)
        assert type(self.ms.account_type) is str

    def test_address_from_bank(self) -> None:
        self.check_with_test_data(key="address_from_bank", test_value=self.ms.address_from_bank)
        assert type(self.ms.address_from_bank) is str

    def test_aod(self) -> None:
        self.check_with_test_data(key="aod", test_value=self.ms.aod)
        assert type(self.ms.aod) is str

    def test_bank_code(self) -> None:
        self.check_with_test_data(key="bank_code", test_value=self.ms.bank_code)
        assert type(self.ms.bank_code) is str

    def test_bank_name(self) -> None:
        self.check_with_test_data(key="bank_name", test_value=self.ms.bank_name)
        assert type(self.ms.bank_name) is str

    def test_branch_code(self) -> None:
        self.check_with_test_data(key="branch_code", test_value=self.ms.branch_code)
        assert type(self.ms.branch_code) is str

    def test_capital(self) -> None:
        self.check_with_test_data(key="capital", test_value=self.ms.capital)
        assert type(self.ms.capital) is str

    def test_citizen_code(self) -> None:
        self.check_with_test_data(key="citizen_code", test_value=self.ms.citizen_code)
        assert type(self.ms.citizen_code) is str

    def test_citizenship_number(self) -> None:
        self.check_with_test_data(key="citizenship_number", test_value=self.ms.citizenship_number)
        assert type(self.ms.citizenship_number) is str

    def test_confirmation_waived(self) -> None:
        self.check_with_test_data(key="confirmation_waived", test_value=self.ms.confirmation_waived)
        assert type(self.ms.confirmation_waived) is str

    def test_contact__from_bank(self) -> None:
        self.check_with_test_data(key="contact__from_bank", test_value=self.ms.contact__from_bank)
        assert type(self.ms.contact__from_bank) is str

    def test_dob(self) -> None:
        self.check_with_test_data(key="dob", test_value=self.ms.dob)
        assert type(self.ms.dob) is str

    def test_dp_name(self) -> None:
        self.check_with_test_data(key="dp_name", test_value=self.ms.dp_name)
        assert type(self.ms.dp_name) is str

    def test_father_mother_name(self) -> None:
        self.check_with_test_data(key="father_mother_name", test_value=self.ms.father_mother_name)
        assert type(self.ms.father_mother_name) is str

    def test_gender__from_bank(self) -> None:
        self.check_with_test_data(key="gender__from_bank", test_value=self.ms.gender__from_bank)
        assert type(self.ms.gender__from_bank) is str

    def test_grandfather_spouse_name(self) -> None:
        self.check_with_test_data(key="grandfather_spouse_name", test_value=self.ms.grandfather_spouse_name)
        assert type(self.ms.grandfather_spouse_name) is str

    def test_issued_date(self) -> None:
        self.check_with_test_data(key="issued_date", test_value=self.ms.issued_date)
        assert type(self.ms.issued_date) is str

    def test_issued_from(self) -> None:
        self.check_with_test_data(key="issued_from", test_value=self.ms.issued_from)
        assert type(self.ms.issued_from) is str

    def test_regex_citizen_number(self) -> None:
        self.check_with_test_data(key="regex_citizen_number", test_value=self.ms.regex_citizen_number)
        assert type(self.ms.regex_citizen_number) is str

    def test_sub_status(self) -> None:
        self.check_with_test_data(key="sub_status", test_value=self.ms.sub_status)
        assert type(self.ms.sub_status) is str

    def test_sub_status_code(self) -> None:
        self.check_with_test_data(key="sub_status_code", test_value=self.ms.sub_status_code)
        assert type(self.ms.sub_status_code) is str

    def test_suspension_flag(self) -> None:
        self.check_with_test_data(key="suspension_flag", test_value=self.ms.suspension_flag)
        assert type(self.ms.suspension_flag) is int

    def test_address(self) -> None:
        self.check_with_test_data(key="address", test_value=self.ms.address)
        assert type(self.ms.address) is str

    def test_boid(self) -> None:
        self.check_with_test_data(key="boid", test_value=self.ms.boid)
        assert type(self.ms.boid) is str

    def test_client_code(self) -> None:
        self.check_with_test_data(key="client_code", test_value=self.ms.client_code)
        assert type(self.ms.client_code) is str

    def test_contact(self) -> None:
        self.check_with_test_data(key="contact", test_value=self.ms.contact)
        assert type(self.ms.contact) is str

    def test_created_approve_date(self) -> None:
        self.check_with_test_data(key="created_approve_date", test_value=self.ms.created_approve_date)
        assert type(self.ms.created_approve_date) is str

    def test_created_approve_date_str(self) -> None:
        self.check_with_test_data(key="created_approve_date_str", test_value=self.ms.created_approve_date_str)
        assert type(self.ms.created_approve_date_str) is str

    def test_customer_type_code(self) -> None:
        self.check_with_test_data(key="customer_type_code", test_value=self.ms.customer_type_code)
        assert type(self.ms.customer_type_code) is str

    def test_demat(self) -> None:
        self.check_with_test_data(key="demat", test_value=self.ms.demat)
        assert type(self.ms.demat) is str

    def test_demat_expiry_date(self) -> None:
        self.check_with_test_data(key="demat_expiry_date", test_value=self.ms.demat_expiry_date)
        assert type(self.ms.demat_expiry_date) is str

    def test_email(self) -> None:
        self.check_with_test_data(key="email", test_value=self.ms.email)
        assert type(self.ms.email) is str

    def test_expired_date(self) -> None:
        self.check_with_test_data(key="expired_date", test_value=self.ms.expired_date)
        assert type(self.ms.expired_date) is str

    def test_expired_date_str(self) -> None:
        self.check_with_test_data(key="expired_date_str", test_value=self.ms.expired_date_str)
        assert type(self.ms.expired_date_str) is str

    def test_gender(self) -> None:
        self.check_with_test_data(key="gender", test_value=self.ms.gender)
        assert type(self.ms.gender) is str

    def test_id(self) -> None:
        self.check_with_test_data(key="id", test_value=self.ms.id)
        assert type(self.ms.id) is int

    def test_image_path(self) -> None:
        self.check_with_test_data(key="image_path", test_value=self.ms.image_path)
        assert type(self.ms.image_path) is str

    def test_mero_share_email(self) -> None:
        self.check_with_test_data(key="mero_share_email", test_value=self.ms.mero_share_email)
        assert type(self.ms.mero_share_email) is str

    def test_name(self) -> None:
        self.check_with_test_data(key="name", test_value=self.ms.name)
        assert type(self.ms.name) is str

    def test_password_change_date(self) -> None:
        self.check_with_test_data(key="password_change_date", test_value=self.ms.password_change_date)
        assert type(self.ms.password_change_date) is str

    def test_password_change_date_str(self) -> None:
        self.check_with_test_data(key="password_change_date_str", test_value=self.ms.password_change_date_str)
        assert type(self.ms.password_change_date_str) is str

    def test_password_expiry_date(self) -> None:
        self.check_with_test_data(key="password_expiry_date", test_value=self.ms.password_expiry_date)
        assert type(self.ms.password_expiry_date) is str

    def test_password_expiry_date_str(self) -> None:
        self.check_with_test_data(key="password_expiry_date_str", test_value=self.ms.password_expiry_date_str)
        assert type(self.ms.password_expiry_date_str) is str

    def test_profile_name(self) -> None:
        self.check_with_test_data(key="profile_name", test_value=self.ms.profile_name)
        assert type(self.ms.profile_name) is str

    def test_render_dashboard(self) -> None:
        self.check_with_test_data(key="render_dashboard", test_value=self.ms.render_dashboard)
        assert type(self.ms.render_dashboard) is bool

    def test_renewed_date(self) -> None:
        self.check_with_test_data(key="renewed_date", test_value=self.ms.renewed_date)
        assert type(self.ms.renewed_date) is str

    def test_renewed_date_str(self) -> None:
        self.check_with_test_data(key="renewed_date_str", test_value=self.ms.renewed_date_str)
        assert type(self.ms.renewed_date_str) is str

    def test_username(self) -> None:
        self.check_with_test_data(key="username", test_value=self.ms.username)
        assert type(self.ms.username) is str

    def test_bank_id_from_bank_list_view(self) -> None:
        self.check_with_test_data(
            key="bank_id_from_bank_list_view",
            test_value=self.ms.bank_id_from_bank_list_view
        )

    def test_bank_code_from_bank_list_view(self) -> None:
        self.check_with_test_data(
            key="bank_code_from_bank_list_view",
            test_value=self.ms.bank_code_from_bank_list_view
        )

    def test_bank_account_branch_from_bank_detail_view(self) -> None:
        self.check_with_test_data(
            key="bank_account_branch_from_bank_detail_view",
            test_value=self.ms.bank_account_branch_from_bank_detail_view
        )

    def test_bank_account_number_from_bank_detail_view(self) -> None:
        self.check_with_test_data(
            key="bank_account_number_from_bank_detail_view",
            test_value=self.ms.bank_account_number_from_bank_detail_view
        )

    def test_bank_id_from_bank_detail_view(self) -> None:
        self.check_with_test_data(
            key="bank_id_from_bank_detail_view",
            test_value=self.ms.bank_id_from_bank_detail_view
        )

    def test_bank_branch_id_from_bank_detail_view(self) -> None:
        self.check_with_test_data(
            key="bank_branch_id_from_bank_detail_view",
            test_value=self.ms.bank_branch_id_from_bank_detail_view
        )

    def test_id_from_bank_detail_view(self) -> None:
        self.check_with_test_data(
            key="id_from_bank_detail_view",
            test_value=self.ms.id_from_bank_detail_view
        )
