package main

import (
	"log"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
	"remote-repo.com/username/repository/chaincode"
)

// https://github.com/hyperledger/fabric-samples/blob/main/asset-transfer-basic/chaincode-go/chaincode/smartcontract_test.go

func main() {
	assetChaincode, err := contractapi.NewChaincode(&chaincode.SmartContract{})
	if err != nil {
		log.Panicf("Error creating asset-transfer-basic chaincode: %v", err)
	}

	if err := assetChaincode.Start(); err != nil {
		log.Panicf("Error starting asset-transfer-basic chaincode: %v", err)
	}
}

/*
func TestInitLedger(t *testing.T) {
	chaincodeStub := &mocks.chaincodeStub{}
	transactionContext := &mocks.TransactionContext{}
	transactionContext.GetStubReturns(chaincodeStub)

	assetTransfer := chaincode.SmartContract{}
	err := assetTransfer.InitLedger(transactionContext)
	require.NoError(t, err)

	chaincodeStub.PutStateReturns(fmt.Errorf("falha ao inserir a chave"))
	err = assetTransfer.InitLedger(transactionContext)
	require.EqualError(t, err, "failed to put to world state. failed inserting key")

}
*/
// simula uma transação de InsertStationData no chaincode BasicCRUD
// func TestInsertStationData(ctx contractapi.TransactionContextInterface, t *testing.T, expected contractChaincodeContract) {
// 	fmt.Println("Inicilizando TestInsertStationData")

// 	// instancia mockStub usando StationDemo como alvo do teste unitario
// 	ctx.GetStub()

// 	stub := ctx.GetStub().GetDecorations()
// }
