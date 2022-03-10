import datetime
import warnings
from typing import List, Optional

import requests

from nepse_tools.platforms.manager import PlatformManager
from nepse_tools.platforms.meroshare import type_hint
from nepse_tools.platforms.meroshare.exceptions import (
    MeroshareDataLoadError,
    MeroshareClientIDNotFoundError,
    MeroshareLoginError,
    MeroshareShareApplicationError,
    MeroshareCredentialChangeError
)
from nepse_tools.utils.session import SessionManager


class MeroShareCore(PlatformManager, SessionManager):
    """
        Class to provide core features like login, session management, logout and
        other variables that is gained from api. Additionally, known backend urls are given
        for making the development process much simpler.
    """

    BASE_URL = "https://webbackend.cdsc.com.np"

    # !! AUTH !!
    # For getting authentication token from backend.
    LOGIN_REQUEST_URL = "https://webbackend.cdsc.com.np/api/meroShare/auth/"
    # For sending logout request to the backend.
    LOGOUT_REQUEST_URL = "https://webbackend.cdsc.com.np/api/meroShare/auth/logout/"
    # Default headers to start with.
    HEADERS = {
        "Connection": "keep-alive",
        "Host": "webbackend.cdsc.com.np",
        "Origin": "https://meroshare.cdsc.com.np",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }
    # !! END AUTH !!

    # !! ADDITIONAL DATA !!
    # :meth:`~MeroShareCore.load_client_id_data`
    GET_CLIENT_IDS_URL = "https://webbackend.cdsc.com.np/api/meroShare/capital/"
    # :meth:`~MeroShareCore.load_initial_data__own_data`
    INITIAL_DATA__OWN_DATA_URL = "https://webbackend.cdsc.com.np/api/meroShare/ownDetail/"
    # :meth:`~MeroShareCore.load_bank_details__my_details`
    BANK_DATA_REQUEST__OWN_DETAIL_URL = "https://webbackend.cdsc.com.np/api/meroShareView/myDetail/{BOID}"
    # :meth:`~MeroShareCore.load_bank_request`
    BANK_REQUEST_URL = "https://webbackend.cdsc.com.np/api/bankRequest/{BANK_CODE}"
    # :meth:`~MeroShareCore.load_bank_list_view`
    BANKS_LIST_VIEW_URL = "https://webbackend.cdsc.com.np/api/meroShare/bank/"
    # :meth:`~MeroShareCore.load_bank_detail_view`
    BANK_DETAIL_VIEW_URL = "https://webbackend.cdsc.com.np/api/meroShare/bank/{BANK_ID}"

    # :meth:`~MeroShareCore.get_account_logs`
    ACTIVITY_LOG_URL = "https://webbackend.cdsc.com.np/api/meroShare/activityLog/search/"

    # :meth:`~MeroShareBase.load_current_share_holdings_symbols`
    CURRENT_SHARE_HOLDINGS_SYMBOLS_URL = "https://webbackend.cdsc.com.np/api/myPurchase/myShare/"

    # !! END ADDITIONAL DATA !!

    # !! APPLICATION, ADDITIONAL DATA !!
    # :meth:`~MeroShareBase.get_applicable_shares`
    APPLICABLE_NEW_IPO_URL = "https://webbackend.cdsc.com.np/api/meroShare/companyShare/applicableIssue/"
    # :meth:`~MeroShareBase.can_apply_to_ipo`
    CAN_APPLY_TO_IPO_CHECK_URL = "https://webbackend.cdsc.com.np/api/meroShare/applicantForm/" \
                                 "customerType/{COMPANY_SHARE_ID}/{DEMAT_NUMBER}"
    # :meth:`~MeroShareBase._apply_for_ipo`
    IPO_APPLICATION_SUBMISSION_URL = "https://webbackend.cdsc.com.np/api/meroShare/applicantForm/share/apply"

    # :meth:`~MeroShareBase._____________` TODO: This one is not used !!
    ABSA_CURRENT_ISSUE_URL = "https://webbackend.cdsc.com.np/api/meroShare/companyShare/currentIssue"
    # :meth:`~MeroShareBase.get_application_reports`
    ABSA_APPLICATION_REPORT_URL = "https://webbackend.cdsc.com.np/api/meroShare/applicantForm/active/search/"
    # :meth:`~MeroShareBase.get_old_application_reports`
    ABSA_OLD_APPLICATION_REPORT_URL = "https://webbackend.cdsc.com.np/api/meroShare/migrated/applicantForm/search/"

    # :meth:`~MeroShareBase.get_ipo_issue_manager_details`
    ABSA_ISSUE_MANAGER_DETAIL_VIEW_URL = "https://webbackend.cdsc.com.np/api/meroShare/active/{COMPANY_SHARE_ID}"

    # :meth:`~MeroShareBase.get_new_applied_ipo_details`
    ABSA_APPLIED_IPO_DETAIL_VIEW_URL = "https://webbackend.cdsc.com.np/api/meroShare/applicantForm/" \
                                       "report/detail/{APPLICATION_FORM_ID}"
    # :meth:`~MeroShareBase.get_old_applied_ipo_details`
    ABSA_OLD_APPLIED_IPO_DETAIL_VIEW_URL = "https://webbackend.cdsc.com.np/api/meroShare/migrated/applicantForm" \
                                           "/report/{APPLICATION_FORM_ID}"
    # !! END APPLICATION, ADDITIONAL DATA !!

    # !! CHANGE PASSWORD !!
    # :meth:`~MeroShareBase.change_password`
    PASSWORD_CHANGE_POST_URL = "https://webbackend.cdsc.com.np/api/meroShare/changePassword/"
    # :meth:`~MeroShareBase.change_pin`
    PIN_CHANGE_POST_URL = "https://webbackend.cdsc.com.np/api/meroShare/changeTransactionPIN/"

    # !! END CHANGE PASSWORD !!

    # !! SHARE HOLDINGS !!
    # :meth:`~MeroShareBase.get_my_shares`
    MY_SHARES_URL = "https://webbackend.cdsc.com.np/api/meroShareView/myShare/"
    # :meth:`~MeroShareBase.get_my_portfolio`
    MY_PORTFOLIO_URL = "https://webbackend.cdsc.com.np/api/meroShareView/myPortfolio/"

    # !! SHARE HOLDINGS !!

    # !! SHARE TRANSACTIONS !!
    # :meth:`~MeroShareBase.get_share_transactions`
    SHARE_TRANSACTIONS_URL = "https://webbackend.cdsc.com.np/api/meroShareView/myTransaction/"

    # !! SHARE TRANSACTIONS !!

    # !! IPO !!
    # :meth:`~MeroShareBase.get_ipo_result_company_list`
    IPO_RESULT_COMPANY_LIST_URL = "https://iporesult.cdsc.com.np/result/companyShares/fileUploaded"
    # :meth:`~MeroShareBase.get_ipo_result`
    IPO_RESULT_CHECK_URL = "https://iporesult.cdsc.com.np/result/result/check"

    # !! IPO !!

    # !! PURCHASE SOURCE !!
    # :meth:`~MeroShareBase.get_share_purchase_source_wacc_not_calculated_details`
    PURCHASE_SOURCE_WACC_NOT_CALCULATED_URL = "https://webbackend.cdsc.com.np/api/myPurchase/search/"
    # :meth:`~MeroShareBase.get_share_purchase_source_wacc_calculated_details`
    PURCHASE_SOURCE_WACC_CALCULATED_URL = "https://webbackend.cdsc.com.np/api/myPurchase/view/"

    # :meth:`~MeroShareBase.do_wacc_calculation_from_wacc_not_calculated_list`
    PURCHASE_SOURCE_WACC_CALCULATION_SUBMISSION_URL = "https://webbackend.cdsc.com.np/api/myPurchase/upload/"

    # !! PURCHASE SOURCE !!

    def __init__(self, dp: str, username: str, password: str, pin: str) -> None:
        """
        Args:
            dp (str): DP used while logging in to meroshare.
            username (str): Username used while logging in to meroshare.
            password (str): Password used while logging in to meroshare.
            pin (str): Pin used when applying to IPO or completing any other transactions.
        """
        super(PlatformManager, self).__init__()
        super(SessionManager, self).__init__()

        self._dp: str = dp
        self._username: str = username
        self.__password: str = password
        self.__pin: str = pin

        self.client_id_data: list[type_hint.ClientIdData] = []

        # ALL NOQA Variables will be defined, it is used here just to make sure we can better linting experience
        self.initial_data__own_data: type_hint.InitialDataOwnData = {}  # NOQA
        self.bank_details__my_details: type_hint.MyDetailsFromBank = {}  # NOQA
        self.bank_request_data: type_hint.BankRequestData = {}  # NOQA
        self.bank_list_view_data: type_hint.BankListView = {}  # NOQA
        self.bank_detail_view_data: type_hint.BankDetailView = {}  # NOQA
        self.current_share_holdings_symbols: Optional[List[str]] = []

        self.is_logged_in = False
        # print(self.bank_detail_view_data[''])

    def hard__load_all_data(self):
        """
        Reloads and caches all data from various All API Endpoint.

        Returns:
            Current Instance of the class
        """

        self.load_client_id_data()
        self.load_initial_data__own_data()
        self.load_bank_details__my_details()
        self.load_bank_request()
        self.load_current_share_holdings_symbols()
        self.load_bank_detail_view()
        return self

    def load_client_id_data(self) -> List[type_hint.ClientIdData]:
        """
        Loads and returns Client ID data as a list, See return data in examples below.

        Returns:
            A List of dictionaries of Client ID data, See more in examples.

        Examples
        --------
        Getting Data from the method.

        >>> self.load_client_id_data()
        [
            {'code': '13200', 'id': 128, 'name': 'ABC SECURITIES PRIVATE LIMITED'},
            {'code': '12300', 'id': 129, 'name': 'AGRAWAL SECURITIES PRIVATE LIMITED'},
            ...
        ]
        """

        client_id_data = self.get(self.GET_CLIENT_IDS_URL)

        if client_id_data.ok:
            self.client_id_data = client_id_data.json()
            return self.client_id_data
        else:
            raise MeroshareDataLoadError(
                f"[!{client_id_data.status_code}!] Error getting data from URL: "
                f"'{client_id_data.url}'\n{client_id_data.text}"
            )

    def load_current_share_holdings_symbols(self) -> List[str]:
        """
        Loads and returns the symbols of all the share that you have, See return data in examples below.

        Returns:
            The symbols of all the share that you have, See more in examples.

        Examples
        --------
        Getting Data from the method.

        >>> self.load_current_share_holdings_symbols()
        ['CCBL', 'DDBL', 'GLH', 'LBBL', 'LEC', 'MLBL', ...]
        """

        resp = self.get(self.CURRENT_SHARE_HOLDINGS_SYMBOLS_URL)

        if resp.ok:
            self.current_share_holdings_symbols = resp.json()
            return self.current_share_holdings_symbols
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def load_current_share_holdings_symbols_if_required(self) -> None:
        """
        calls `MeroShareCore.current_share_holdings_symbols` if data is not already fetched.

        Returns:
            None
        """

        if not self.current_share_holdings_symbols:
            self.load_current_share_holdings_symbols()

    def load_initial_data__own_data(self) -> type_hint.InitialDataOwnData:
        """
        Loads and returns the initial data from meroshare API. See more in examples

        Returns:
            initial data from meroshare API, See more in examples.

        Examples
        --------
        Getting Data from the method.

        >>> self.load_initial_data__own_data()
        {
            address: str,
            boid: str,
            clientCode: str,
            contact: str,
            createdApproveDate: str,
            createdApproveDateStr: str,
            customerTypeCode: str,
            demat: str,
            dematExpiryDate: str,
            email: str,
            gender: str,
            id: int,
            imagePath: str,
            meroShareEmail: str,
            name: str,
            passwordChangeDate: str,
            passwordChangedDateStr: str,
            passwordExpiryDate: str,
            passwordExpiryDateStr: str,
            profileName: str,
            renderDashboard: bool,
            renewedDate: str,
            renewedDateStr: str,
            username: str,
            expiredDate: str,
            expiredDateStr: str,
        }
        """

        own_data = self.get(self.INITIAL_DATA__OWN_DATA_URL)

        if own_data.ok:
            self.initial_data__own_data = own_data.json()
            return self.initial_data__own_data
        else:
            raise MeroshareDataLoadError(
                f"[!{own_data.status_code}!] Error getting data from URL: '{own_data.url}'\n{own_data.text}"
            )

    def load_initial_data__own_data_if_required(self) -> None:
        """
        Loads `initial_data__own_data` own data if not already loaded

        Returns:
            None
        """

        if not self.initial_data__own_data:
            self.load_initial_data__own_data()

    def load_bank_details__my_details(self) -> type_hint.MyDetailsFromBank:
        """
        Loads and returns the user's details from bank, See return data in examples below.

        Returns:
            user's details from bank, See more in examples.

        Examples
        --------
        Getting Data from the method.

        >>> self.load_bank_details__my_details()
        {
            accountNumber: str,
            accountOpenDate: str,
            accountStatus: int,
            accountStatusFlag: str,
            accountStatusName: str,
            accountType: str,
            address: str,
            aod: str,
            bankCode: str,
            bankName: str,
            boid: str,
            branchCode: str,
            capital: str,
            citizenCode: str,
            citizenshipNumber: str,
            confirmationWaived: str,
            contact: str,
            dob: str,
            dpName: str,
            fatherMotherName: str,
            gender: str,
            grandfatherSpouseName: str,
            issuedDate: str,
            issuedFrom: str,
            name: str,
            regexCitizenNumber: str,
            subStatus: str,
            subStatusCode: str,
            suspensionFlag: int
        }
        """

        bank_details = self.get(
            self.BANK_DATA_REQUEST__OWN_DETAIL_URL.format(BOID=self.demat)
        )

        if bank_details.ok:
            self.bank_details__my_details = bank_details.json()
            return self.bank_details__my_details
        else:
            raise MeroshareDataLoadError(
                f"[!{bank_details.status_code}!] Error getting data from URL: '{bank_details.url}'\n{bank_details.text}"
            )

    def load_bank_details__my_details_if_required(self) -> None:
        """
        Loads `bank_details__my_details` own data if not already loaded

        Returns:
            None
        """

        if not self.bank_details__my_details:
            self.load_bank_details__my_details()

    def load_bank_request(self) -> type_hint.BankRequestData:
        """
        Loads and returns a lot of data from meroshare's bank data api, See return data in examples below.

        Returns:
            data from the bank data request api

        Examples
        --------
        Getting Data from the method.

        >>> self.load_bank_request()
        {
            accountBranch: dict,
            accountName: str,
            accountNumber: str,
            bank: dict,
            boid: str,
            branch: dict,
            capital: dict,
            createdBy: dict,
            createdDate: str,
            crnNumber: str,
            id: int,
            kycDetail: dict,
            modifiedBy: dict,
            name: str,
            status: dict
        }
        """

        bank_request = self.get(
            self.BANK_REQUEST_URL.format(BANK_CODE=self.bank_code)
        )

        if bank_request.ok:
            self.bank_request_data = bank_request.json()
            return self.bank_request_data
        else:
            raise MeroshareDataLoadError(
                f"[!{bank_request.status_code}!] Error getting data from URL: '{bank_request.url}'\n{bank_request.text}"
            )

    def load_bank_request_if_required(self) -> None:
        """
        Loads `bank_request` own data if not already loaded

        Returns:
            None
        """
        if not self.bank_request_data:
            self.load_bank_request()

    def load_bank_list_view(self) -> type_hint.BankListView:
        """
        Loads and returns the first bank detail from the meroshare api, See return data in examples below.

        Returns:
            first bank detail from the meroshare api, See more in examples.

        Examples
        --------
        Getting Data from the method.

        >>> self.load_bank_list_view()
        {
            'code': str,
            'id': int,
            'name': str
        }
        """

        resp = self.get(self.BANKS_LIST_VIEW_URL)

        if resp.ok:
            data = resp.json()
            self.bank_list_view_data = data[0] if data else []
            return self.bank_list_view_data
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}"
            )

    def load_bank_list_view_if_required(self) -> None:
        """
        Loads `bank_list_view` own data if not already loaded

        Returns:
            None
        """

        if not self.bank_list_view_data:
            self.load_bank_list_view()

    def load_bank_detail_view(self) -> type_hint.BankDetailView:
        """
        Loads and returns the detail data about current user's account bank, See return data in examples below.

        Returns:
            detail data about current user's account bank, See more in examples.

        Examples
        --------
        Getting Data from the method.

        >>> self.load_bank_detail_view()
        {
            accountBranchId: int,
            accountNumber: str,
            bankId: int,
            branchID: int,
            branchName: str,
            id: int
        }
        """

        resp = self.get(self.BANK_DETAIL_VIEW_URL.format(BANK_ID=self.bank_id_from_bank_list_view))

        if resp.ok:
            self.bank_detail_view_data = resp.json()
            return self.bank_detail_view_data
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}"
            )

    def load_bank_detail_view_if_required(self) -> None:
        """
        Loads `bank_detail_view` own data if not already loaded

        Returns:
            None
        """

        if not self.bank_detail_view_data:
            self.load_bank_detail_view()

    @property
    def current_share_holdings_symbols_lazy(self) -> List[str]:
        self.load_current_share_holdings_symbols_if_required()
        return self.current_share_holdings_symbols

    @property
    def bank_id_from_bank_list_view(self) -> int:
        self.load_bank_list_view_if_required()
        return self.bank_list_view_data.get("id")

    @property
    def bank_code_from_bank_list_view(self) -> str:
        self.load_bank_list_view_if_required()
        return self.bank_list_view_data.get("code")

    @property
    def bank_account_branch_from_bank_detail_view(self) -> int:
        self.load_bank_detail_view_if_required()
        return self.bank_detail_view_data.get("accountBranchId")

    @property
    def bank_account_number_from_bank_detail_view(self) -> str:
        self.load_bank_detail_view_if_required()
        return self.bank_detail_view_data.get("accountNumber")

    @property
    def bank_id_from_bank_detail_view(self) -> int:
        self.load_bank_detail_view_if_required()
        return self.bank_detail_view_data.get("bankId")

    @property
    def bank_branch_id_from_bank_detail_view(self) -> int:
        self.load_bank_detail_view_if_required()
        return self.bank_detail_view_data.get("branchID")

    @property
    def id_from_bank_detail_view(self) -> int:
        self.load_bank_detail_view_if_required()
        print(self.bank_detail_view_data["id"])
        return self.bank_detail_view_data.get("id")

    @property
    def bank_branch(self) -> str:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("accountBranch", {}).get("name")

    @property
    def bank_branch_code(self) -> str:
        self.load_bank_request_if_required()
        return str(self.bank_request_data.get("accountBranch", {}).get("code"))

    @property
    def bank_branch_id(self) -> int:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("accountBranch", {}).get("id")

    @property
    def bank_id(self) -> int:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("bank", {}).get("id")

    @property
    def capital_code(self) -> str:
        self.load_bank_request_if_required()
        return str(self.bank_request_data.get("capital", {}).get("code"))

    @property
    def capital_id(self):
        self.load_bank_request_if_required()
        return self.bank_request_data.get("capital", {}).get("id")

    @property
    def capital_name(self) -> str:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("capital", {}).get("name")

    @property
    def account_creation_detail(self) -> dict | None:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("createdBy")

    @property
    def crn_number(self) -> str:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("crnNumber")

    @property
    def kyc_detail(self) -> dict | None:
        self.load_bank_request_if_required()
        return self.bank_request_data.get("kycDetail")

    @property
    def account_number(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("accountNumber")

    @property
    def account_open_date(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("accountOpenDate")

    @property
    def account_status(self) -> int:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("accountStatus")

    @property
    def account_status_flag(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("accountStatusFlag")

    @property
    def account_status_name(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("accountStatusName")

    @property
    def account_type(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("accountType")

    @property
    def address_from_bank(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("address")

    @property
    def aod(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("aod")

    @property
    def bank_code(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("bankCode")

    @property
    def bank_name(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("bankName")

    @property
    def branch_code(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("branchCode")

    @property
    def capital(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("capital")

    @property
    def citizen_code(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("citizenCode")

    @property
    def citizenship_number(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("citizenshipNumber")

    @property
    def confirmation_waived(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("confirmationWaived")

    @property
    def contact__from_bank(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("contact")

    @property
    def dob(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("dob")

    @property
    def dp_name(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("dpName")

    @property
    def father_mother_name(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("fatherMotherName")

    @property
    def gender__from_bank(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("gender")

    @property
    def grandfather_spouse_name(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("grandfatherSpouseName")

    @property
    def issued_date(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("issuedDate")

    @property
    def issued_from(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("issuedFrom")

    @property
    def regex_citizen_number(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("regexCitizenNumber")

    @property
    def sub_status(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("subStatus")

    @property
    def sub_status_code(self) -> str:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("subStatusCode")

    @property
    def suspension_flag(self) -> int:
        self.load_bank_details__my_details_if_required()
        return self.bank_details__my_details.get("suspensionFlag")

    @property
    def address(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("address")

    @property
    def boid(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("boid")

    @property
    def client_code(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("clientCode")

    @property
    def contact(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("contact")

    @property
    def created_approve_date(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("createdApproveDate")

    @property
    def created_approve_date_str(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("createdApproveDateStr")

    @property
    def customer_type_code(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("customerTypeCode")

    @property
    def demat(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("demat")

    @property
    def demat_expiry_date(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("dematExpiryDate")

    @property
    def email(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("email")

    @property
    def expired_date(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("expiredDate")

    @property
    def expired_date_str(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("expiredDateStr")

    @property
    def gender(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("gender")

    @property
    def id(self) -> int:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("id")

    @property
    def image_path(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("imagePath")

    @property
    def mero_share_email(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("meroShareEmail")

    @property
    def name(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("name")

    @property
    def password_change_date(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("passwordChangeDate")

    @property
    def password_change_date_str(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("passwordChangedDateStr")

    @property
    def password_expiry_date(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("passwordExpiryDate")

    @property
    def password_expiry_date_str(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("passwordExpiryDateStr")

    @property
    def profile_name(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("profileName")

    @property
    def render_dashboard(self) -> bool:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("renderDashboard")

    @property
    def renewed_date(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("renewedDate")

    @property
    def renewed_date_str(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("renewedDateStr")

    @property
    def username(self) -> str:
        self.load_initial_data__own_data_if_required()
        return self.initial_data__own_data.get("username")

    # ==================AUTH=================
    def get_client_id(self) -> int | None:
        """
        Gets client ID using dp

        Returns:
            client id

        """
        if not self.client_id_data:
            self.load_client_id_data()

        for capital_detail in self.client_id_data:
            if capital_detail.get("code") == self._dp:
                return capital_detail.get("id")

        raise MeroshareClientIDNotFoundError(f"[!] Error getting client id for DP: '{self._dp}'")

    def login(self) -> dict:
        """
        Logs in the user
        
        Returns:
            login response from meroshare
        """
        login_resp = self.post(
            self.LOGIN_REQUEST_URL,
            json={
                "clientId": self.get_client_id(),
                "username": self._username,
                "password": self.__password
            }
        )

        if login_resp.ok:
            self.is_logged_in = True

            self.session_headers = {
                **self.session_headers,
                "Authorization": login_resp.headers.get("Authorization")
            }
            return login_resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{login_resp.status_code}!] Error getting data from URL: '{login_resp.url}'\n{login_resp.text}"
            )

    def logout(self) -> dict:
        """
        Logs out the user

        Returns:
            Logout response from meroshare
        """
        resp = self.get(self.LOGOUT_REQUEST_URL)

        if resp.ok:
            self.is_logged_in = False
            self.session_headers = self.HEADERS

            return resp.json()
        else:
            raise MeroshareLoginError(
                f"[!{resp.status_code}!] Error Logging in:\n{resp.text}"
            )

    # !==================END AUTH=================!


class MeroShareBase(MeroShareCore):
    # ==================APPLY AND UPDATE IPO=================
    def can_apply_to_ipo(self, ipo_id: int) -> bool:
        resp = self.get(
            self.CAN_APPLY_TO_IPO_CHECK_URL.format(
                COMPANY_SHARE_ID=ipo_id,
                DEMAT_NUMBER=self.demat
            )
        )

        if resp.ok and resp.json().get("message") == "Customer can apply.":
            return True
        return False

    def get_applicable_shares(self) -> dict:
        resp = self.post(
            self.APPLICABLE_NEW_IPO_URL,
            json={
                "filterFieldParams": [
                    {"key": "companyIssue.companyISIN.script", "alias": "Scrip"},
                    {"key": "companyIssue.companyISIN.company.name", "alias": "Company Name"},
                    {"key": "companyIssue.assignedToClient.name", "value": "", "alias": "Issue Manager"}
                ],
                "page": 1,
                "size": 10,
                "searchRoleViewConstants": "VIEW_APPLICABLE_SHARE",
                "filterDateParams": [
                    {"key": "minIssueOpenDate", "condition": "", "alias": "", "value": ""},
                    {"key": "maxIssueCloseDate", "condition": "", "alias": "", "value": ""}
                ]
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}"
            )

    def _apply_for_ipo(self, payload: dict):
        resp = self.post(self.IPO_APPLICATION_SUBMISSION_URL, json=payload)

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareShareApplicationError(
                f"[!{resp.status_code}!] Error getting data from URL: "
                f"'{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    def apply_for_ipo(
            self, company_share_id: int = None, scrip: str = None, auto_apply_all: bool = False,
            number_of_shares: int = 10
    ) -> list[dict] | None:
        applicable_shares = self.get_applicable_shares().get("object", [])
        responses = []

        if company_share_id and scrip:
            warnings.warn(
                f"Only one field is allowed but provided both: "
                f"`{company_share_id=}` and `{scrip=}`. Using `{company_share_id=}` as default"
            )
        if not company_share_id and not scrip and auto_apply_all is False:
            raise ValueError(f"One of the parameter must be given. {company_share_id=}, {scrip=}, {company_share_id=}")

        for applicable_share in applicable_shares:
            if (
                    auto_apply_all is True
            ) or (
                    applicable_share.get("companyShareId") == company_share_id
                    or applicable_share.get("scrip") == scrip
            ):
                if self.can_apply_to_ipo(applicable_share.get("companyShareId")):
                    responses.append(
                        self._apply_for_ipo(
                            payload={
                                "accountBranchId": self.bank_branch_id,
                                "accountNumber": self.bank_account_number_from_bank_detail_view,
                                "appliedKitta": str(number_of_shares),
                                "bankId": self.bank_id_from_bank_list_view,
                                "boid": self.boid,
                                "companyShareId": str(applicable_share.get("companyShareId")),
                                "crnNumber": self.crn_number,
                                "customerId": self.id_from_bank_detail_view,
                                "demat": self.demat,
                                "transactionPIN": self.__pin,
                            }
                        )
                    )

        return responses

    # !==================END APPLY AND UPDATE IPO=================!

    # ==================ABSA RELATED=================
    def get_application_reports(self, page: int = 1, size: int = 200):
        resp = self.post(
            self.ABSA_APPLICATION_REPORT_URL,
            json={
                "filterFieldParams": [
                    {"key": "companyShare.companyIssue.companyISIN.script", "alias": "Scrip"},
                    {"key": "companyShare.companyIssue.companyISIN.company.name", "alias": "Company Name"}
                ],
                "page": page,
                "size": size,
                "searchRoleViewConstants": "VIEW_APPLICANT_FORM_COMPLETE",
                "filterDateParams": [
                    {"key": "appliedDate", "condition": "", "alias": "", "value": ""},
                    {"key": "appliedDate", "condition": "", "alias": "", "value": ""}
                ]
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    def get_old_application_reports(self, page: int = 1, size: int = 200):
        resp = self.post(
            self.ABSA_OLD_APPLICATION_REPORT_URL,
            json={
                "filterFieldParams": [
                    {"key": "companyShare.companyIssue.companyISIN.script", "alias": "Scrip"},
                    {"key": "companyShare.companyIssue.companyISIN.company.name", "alias": "Company Name"}
                ],
                "page": page,
                "size": size,
                "searchRoleViewConstants": "VIEW",
                "filterDateParams": [
                    {"key": "appliedDate", "condition": "", "alias": "", "value": ""},
                    {"key": "appliedDate", "condition": "", "alias": "", "value": ""}
                ]
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    def get_ipo_issue_manager_details(self, company_share_id: int):
        resp = self.get(
            self.ABSA_ISSUE_MANAGER_DETAIL_VIEW_URL.format(COMPANY_SHARE_ID=company_share_id)
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    def get_new_applied_ipo_details(self, application_form_id: int):
        resp = self.get(
            self.ABSA_APPLIED_IPO_DETAIL_VIEW_URL.format(APPLICATION_FORM_ID=application_form_id)
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def get_old_applied_ipo_details(self, application_form_id: int):
        resp = self.get(
            self.ABSA_OLD_APPLIED_IPO_DETAIL_VIEW_URL.format(APPLICATION_FORM_ID=application_form_id)
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def get_applied_ipo_details(self, application_form_id: int):
        try:
            return self.get_new_applied_ipo_details(application_form_id)
        except MeroshareDataLoadError:
            return self.get_old_applied_ipo_details(application_form_id)

    # !==================ABSA RELATED=================!

    # ==================CHANGING ACCOUNT DETAILS=================
    def change_password(self, new_password: str):
        resp = self.post(
            self.PASSWORD_CHANGE_POST_URL,
            json={
                "newPassword": new_password,
                "confirmPassword": new_password,
                "oldPassword": self.__password,
            }
        )

        if resp.ok:
            self.__password = new_password
            return resp.json()
        else:
            raise MeroshareCredentialChangeError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    def change_pin(self, new_pin: int):
        resp = self.post(
            self.PIN_CHANGE_POST_URL,
            json={
                "oldTransactionPIN": self.__password,
                "newTransactionPIN": str(new_pin),
                "confirmTransactionPIN": str(new_pin),
            }
        )

        if resp.ok:
            self.__pin = new_pin
            return resp.json()
        else:
            raise MeroshareCredentialChangeError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    # !==================CHANGING ACCOUNT DETAILS=================!

    # ==================GETTING ACCOUNT LOGS=================
    def get_account_logs(
            self, start_date: datetime.date, end_date: datetime.date, result_size: int = 200,
            page: int = 1
    ):
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        resp = self.post(
            self.ACTIVITY_LOG_URL,
            json={
                "filterFieldParams": [
                    {"key": "browserName"}
                ],
                "page": page,
                "size": result_size,
                "searchRoleViewConstants": "VIEW",
                "filterDateParams": [
                    {
                        "key": "recordedDate", "condition": "", "alias": "",
                        "value": f"BETWEEN '{start_date}' AND '{end_date} 23:59:59'"
                    },
                    {"key": "recordedDate", "condition": "", "alias": "", "value": ""}
                ]
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    # !==================END GETTING ACCOUNT LOGS=================!

    # ===================GETTING MY SHARE HOLDINGS DETAILS==================
    def get_my_shares(
            self,
            sort_by: str = "CCY_SHORT_NAME",
            page: int = 1,
            size: int = 200,
            sort_asc: bool = True
    ) -> list[dict]:
        resp = self.post(
            self.MY_SHARES_URL,
            json={
                "sortBy": sort_by,
                "demat": [self.demat],
                "clientCode": str(self.client_code),
                "page": page,
                "size": size,
                "sortAsc": sort_asc
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    def get_my_portfolio(
            self,
            sort_by: str = "script",
            page: int = 1,
            size: int = 200,
            sort_asc: bool = True
    ) -> list[dict]:
        resp = self.post(
            self.MY_PORTFOLIO_URL,
            json={
                "sortBy": sort_by,
                "demat": [str(self.demat)],
                "clientCode": self.client_code,
                "page": page,
                "size": size,
                "sortAsc": sort_asc
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    # !==================GETTING MY SHARE HOLDINGS DETAILS=================!

    # ==================GETTING SHARE TRANSACTION DETAILS=================
    def get_share_transactions(self, symbol: str = None, page: int = 1, size: int = 200):
        resp = self.post(
            self.SHARE_TRANSACTIONS_URL,
            json={
                "boid": str(self.demat),
                "clientCode": str(self.client_code),
                "script": symbol,
                "fromDate": None,
                "toDate": None,
                "requestTypeScript": False if symbol is None else True,
                "page": page,
                "size": size
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp.json()
            )

    # !==================GETTING SHARE TRANSACTION DETAILS=================!

    # ===================GETTING SHARE PURCHASE SOURCE DETAILS==================
    def get_share_purchase_source_wacc_not_calculated_details(self, symbol: str) -> List[dict]:
        resp = self.post(
            self.PURCHASE_SOURCE_WACC_NOT_CALCULATED_URL,
            json={
                "demat": self.demat,
                "scrip": symbol.upper()
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def get_share_purchase_source_wacc_calculated_details(self, symbol: str) -> dict:
        resp = self.post(
            self.PURCHASE_SOURCE_WACC_CALCULATED_URL,
            json={
                "demat": self.demat,
                "scrip": symbol.upper()
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def do_wacc_calculation_from_wacc_not_calculated_list(self, wacc_not_calculated_list_data: list[dict]) -> dict:
        if not wacc_not_calculated_list_data:
            raise ValueError(f"`{wacc_not_calculated_list_data=}` cant be a empty list.")

        resp = self.post(
            self.PURCHASE_SOURCE_WACC_CALCULATION_SUBMISSION_URL,
            json=wacc_not_calculated_list_data
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def do_wacc_calculation_from_company_symbol(self, symbol: str) -> dict:
        return self.do_wacc_calculation_from_wacc_not_calculated_list(
            self.get_share_purchase_source_wacc_not_calculated_details(symbol)
        )

    # !==================GETTING SHARE PURCHASE SOURCE DETAILS=================!

    # ===================GETTING IPO RESULTS==================
    def get_ipo_result_company_list(self):
        resp = self.get(self.IPO_RESULT_COMPANY_LIST_URL)

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    def get_ipo_result(self, company_share_id: int) -> dict:
        resp = requests.post(
            self.IPO_RESULT_CHECK_URL,
            json={
                "companyShareId": company_share_id,
                "boid": self.demat
            }
        )

        if resp.ok:
            return resp.json()
        else:
            raise MeroshareDataLoadError(
                f"[!{resp.status_code}!] Error getting data from URL: '{resp.url}'\n{resp.text}",
                error_data=resp
            )

    # !==================GETTING IPO RESULTS=================!


class MeroShare(MeroShareBase):
    pass
