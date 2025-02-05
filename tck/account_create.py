import utils

from jsonrpcserver import method, Success
from hiero_sdk_python.account.account_create_transaction import AccountCreateTransaction
from key_identifier import KeyIdentifier

# NOTE: The problem is I need to use a string to identify whether or not a key is ecdsa, ed25519, public or private
#  The PrivateKey class has a 'from_string' class which I can take advantage of easily
#  The PublicKey doesnt have anything helpful, once you have a reference to it you can check if it is ed25519 or ecdsa
#  So I will likely have to add a way to check for the public key, this can be done outside of the PublicKey class,
#   but to keep consistency with the PrivateKey class it would be really nice to have a 'from_string' class in there
#   Ill take a look into it rn to see if it is something I am capable of doing well (I know a way I could but its dookie)
#   It doesnt look like something that I really have any right doing, Im not really sure where to start with the ec key,
#   I'll look into it again
#  Ignoring KeyLists right now
#  The """...""" block is taken directly from the tck AccountCreateTransaction.md & combined with the intellij
#   autogenerated """...""" block
@method
def createAccount(key: str = None, initialBalance: str = None, receiverSignatureRequired: bool = None, autoRenewPeriod: str = None,
    memo: str = None, maxAutoTokenAssociations: int = None, stakedAccountId: str = None, stakedNodeId: str = None,
    declineStakingReward: bool = None, alias: str = None, commonTransactionParams: dict = None):
    """
    :param key: string, optional, DER-encoded hex string representation for private or public keys. Keylists and threshold keys are the hex of the serialized protobuf bytes.
    :param initialBalance: Units of tinybars, optional
    :param receiverSignatureRequired: bool, optional
    :param autoRenewPeriod: string, Units of seconds, optional
    :param memo: string, optional
    :param maxAutoTokenAssociations: int32, optional
    :param stakedAccountId: string, optional
    :param stakedNodeId: string, optional
    :param declineStakingReward: bool, optional
    :param alias: string, optional, Hex string representation of the keccak-256 hash of an ECDSAsecp256k1 public key type.
    :param commonTransactionParams: JSON object, optional

    :return accountId: string, The ID of the created account.
    :return status:	string, The status of the submitted AccountCreateTransaction (from a TransactionReceipt).
    """
    key_and_public = KeyIdentifier.identify(key)

    if key_and_public[1] is False:
        public_key = key_and_public[0].public_key()
    else:
        public_key = key_and_public[0]

    # TODO: add all of the other transaction parameters
    transaction = (
        AccountCreateTransaction()
        .set_key(public_key)
        .set_account_memo(memo)
        .freeze_with(utils.__client)
    )
    # WARNING: I believe that this is right, but im not sure what the case is if the key parameter is a Private Key
    #  why the heck are they giving me a private key anyways...
    transaction.sign(utils.__operatorPrivateKey)
    receipt = transaction.execute(utils.__client)

    return Success({
        "accountId": receipt.accountId,
        "status": receipt.status,
    })
