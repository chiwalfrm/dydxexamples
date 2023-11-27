"""
Generates the OrderId provided by the Indexer,
deterministically from an OrderId. This way
the trader can easily join placement-time data
to their fills.
"""

from dataclasses import dataclass
import uuid

namespace_str = "0f9da948-a6fb-4c45-9edc-4685c3f3317d" # https://github.com/dydxprotocol/v4-chain/blob/29d1517/indexer/packages/postgres/src/helpers/uuid.ts#L4
NAMESPACE = uuid.UUID(namespace_str)

@dataclass
class SubaccountId:
    owner: str  # The address of the wallet that owns this subaccount
    number: int # The subaccount number, usually 0

def subaccount_id_to_uuid(subaccount_id: SubaccountId):
    """
    Based off of the following typescript.

    https://github.com/dydxprotocol/v4-chain/blob/29d1517/indexer/packages/postgres/src/stores/subaccount-table.ts#L29

    ```ts
    export function subaccountIdToUuid(subaccountId: IndexerSubaccountId): string {
        return uuid(subaccountId.owner, subaccountId.number);
    }
    ```
    """
    buffer_value = f"{subaccount_id.owner}-{subaccount_id.number}" # Buffer.from(`${address}-${subaccountNumber}`, BUFFER_ENCODING_UTF_8)
    return uuid.uuid5(
        namespace=NAMESPACE,
        name=buffer_value,
    )

@dataclass
class IndexerOrderId:
    subaccount_id: SubaccountId
    client_id: int
    clob_pair_id: int
    order_flags: int


def make_order_id_uuid(indexer_order_id: IndexerOrderId):
    """
    Based off of the following typescript.
    
    ```ts
    export function uuid(
        subaccountId: string,
        clientId: string,
        clobPairId: string,
        orderFlags: string,
    ): string {
        // TODO(IND-483): Fix all uuid string substitutions to use Array.join.
        return getUuid(
            Buffer.from(
            `${subaccountId}-${clientId}-${clobPairId}-${orderFlags}`,
            BUFFER_ENCODING_UTF_8,
            ),
        );
    }
    export function orderIdToUuid(orderId: IndexerOrderId): string {
        return uuid(
            SubaccountTable.subaccountIdToUuid(orderId.subaccountId!),
            orderId.clientId.toString(),
            orderId.clobPairId.toString(),
            orderId.orderFlags.toString(),
        );
        }
    ```
    """
    subaccount_uuid = subaccount_id_to_uuid(subaccount_id=indexer_order_id.subaccount_id)
    name_str = f"{subaccount_uuid}-{indexer_order_id.client_id}-{indexer_order_id.clob_pair_id}-{indexer_order_id.order_flags}"
    order_id_uuid = uuid.uuid5(
        namespace=NAMESPACE,
        name=name_str,
    )

    return order_id_uuid

def make_example_order_id() -> IndexerOrderId:
    return IndexerOrderId(
        subaccount_id=SubaccountId(owner="dydx1ncxtg3lycfwg8w9f2ymrjzjzx30hjmtrmrccny", number=0),
        client_id=101_010,
        clob_pair_id=5,
        order_flags=0, # short term order
    )

if __name__ == "__main__":
    example_order_id = make_example_order_id()
    order_id_uuid = make_order_id_uuid(example_order_id)
    print(f"Order UUID: {order_id_uuid}")
