"""
Contains typehint for meroshare package.

Contribution:
    If you need to create any typehint that will be primarily used in meroshare then, it must go here.
"""

import typing


class ClientIdData(typing.TypedDict):
    """
    Dict typehint for client id data.
    """
    code: str
    id: int
    name: str


class InitialDataOwnData(typing.TypedDict):
    """
    Dict typehint for the data that initially loads.
    """
    address: str
    boid: str
    clientCode: str
    contact: str
    createdApproveDate: str
    createdApproveDateStr: str
    customerTypeCode: str
    demat: str
    dematExpiryDate: str
    email: str
    gender: str
    id: int
    imagePath: str
    meroShareEmail: str
    name: str
    passwordChangeDate: str
    passwordChangedDateStr: str
    passwordExpiryDate: str
    passwordExpiryDateStr: str
    profileName: str
    renderDashboard: bool
    renewedDate: str
    renewedDateStr: str
    username: str
    expiredDate: str
    expiredDateStr: str


class MyDetailsFromBank(typing.TypedDict):
    """
    Dict typehint for my details from bank.
    """
    accountNumber: str
    accountOpenDate: str
    accountStatus: int
    accountStatusFlag: str
    accountStatusName: str
    accountType: str
    address: str
    aod: str
    bankCode: str
    bankName: str
    boid: str
    branchCode: str
    capital: str
    citizenCode: str
    citizenshipNumber: str
    confirmationWaived: str
    contact: str
    dob: str
    dpName: str
    fatherMotherName: str
    gender: str
    grandfatherSpouseName: str
    issuedDate: str
    issuedFrom: str
    name: str
    regexCitizenNumber: str
    subStatus: str
    subStatusCode: str
    suspensionFlag: int


class BankRequestData(typing.TypedDict):
    """
    Dict typehint for data from bank request data.
    """
    accountBranch: dict
    accountName: str
    accountNumber: str
    bank: dict
    boid: str
    branch: dict
    capital: dict
    createdBy: dict
    createdDate: str
    crnNumber: str
    id: int
    kycDetail: dict
    modifiedBy: dict
    name: str
    status: dict


class BankListView(typing.TypedDict):
    """
    Dict Typehint for data gained about users bank.
    """
    code: str
    id: int
    name: str


class BankDetailView(typing.TypedDict):
    """
    Dict Typehint for detailed data gained from bank.
    """
    accountBranchId: int
    accountNumber: str
    bankId: int
    branchID: int
    branchName: str
    id: int
