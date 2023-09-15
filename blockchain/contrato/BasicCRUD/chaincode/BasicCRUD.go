package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing an Asset
type SmartContract struct {
	contractapi.Contract
}

// Asset describes basic details of what makes up a simple asset
type Asset struct {
	ID             string `json:"ID"`
	Color          string `json:"color"`
	Size           int    `json:"size"`
	Owner          string `json:"owner"`
	AppraisedValue int    `json:"appraisedValue"`
}

// identificador será station id
type StationData struct {
	DeviceName          string `json:"name"`
	DeviceType          string `json:"devicetype"`
	Unit                string `json:"unit"`
	Values              string `json:"values"`
	LastUpdateUnix      string `json:"lastupdateunix"`
	ClientExecutionUnix string `json:"clientexecutionunix"`
	// credits 
}

// InitLedger adds a base set of assets to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	assets := []Asset{
		{ID: "asset1", Color: "blue", Size: 5, Owner: "Tomoko", AppraisedValue: 300},
		{ID: "asset2", Color: "red", Size: 5, Owner: "Brad", AppraisedValue: 400},
		{ID: "asset3", Color: "green", Size: 10, Owner: "Jin Soo", AppraisedValue: 500},
		{ID: "asset4", Color: "yellow", Size: 10, Owner: "Max", AppraisedValue: 600},
		{ID: "asset5", Color: "black", Size: 15, Owner: "Adriana", AppraisedValue: 700},
		{ID: "asset6", Color: "white", Size: 15, Owner: "Michel", AppraisedValue: 800},
	}

	for _, asset := range assets {
		assetJSON, err := json.Marshal(asset)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(asset.ID, assetJSON)

		if err != nil {
			return fmt.Errorf("failed to put to world state. %v", err)
		}
	}

	return nil
}

// CreateAsset issues a new asset to the world state with given details.
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, id string, color string, size int, owner string, appraisedValue int) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

	asset := Asset{
		ID:             id,
		Color:          color,
		Size:           size,
		Owner:          owner,
		AppraisedValue: appraisedValue,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// ReadAsset returns the asset stored in the world state with given id.
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, id string) (*Asset, error) {

	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// UpdateAsset updates an existing asset in the world state with provided parameters.
func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, id string, color string, size int, owner string, appraisedValue int) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	// overwriting original asset with new asset
	asset := Asset{
		ID:             id,
		Color:          color,
		Size:           size,
		Owner:          owner,
		AppraisedValue: appraisedValue,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// DeleteAsset deletes an given asset from the world state.
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, id string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	return ctx.GetStub().DelState(id)
}

// AssetExists returns true when asset with given ID exists in world state
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// TransferAsset updates the owner field of asset with given id in world state.
func (s *SmartContract) TransferAsset(ctx contractapi.TransactionContextInterface, id string, newOwner string) error {
	asset, err := s.ReadAsset(ctx, id)
	if err != nil {
		return err
	}

	asset.Owner = newOwner
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// GetAllAssets returns all assets found in world state
func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}

const compositeKey = ""

// chave composta id e timestamp unix
func (s *SmartContract) InsertStationData(ctx contractapi.TransactionContextInterface,
	stationid string,
	devicename string,
	devicetype string,
	unit string,
	values string,
	lastupdateunix string,
	clientexecutionunix string,
) error {

	stationdata := StationData{
		DeviceName:          devicename,
		DeviceType:          devicetype,
		Unit:                unit,
		Values:              values,
		LastUpdateUnix:      lastupdateunix,
		ClientExecutionUnix: clientexecutionunix,
	}

	stationdataJSON, err := json.Marshal(stationdata)
	if err != nil {
		return err
	}

	// chave composta
	key, err := ctx.GetStub().CreateCompositeKey(compositeKey, []string{stationid, devicename})

	// verifica se já existe com a mesma chave composta (id e updatetimeunix)
	// exists, err := s.AssetExists(ctx, key)
	// if err != nil {
	// 	return err
	// }

	// if exists {
	// 	return fmt.Errorf("o objeto %s já existe com o mesmo id", key)
	// }

	return ctx.GetStub().PutState(key, stationdataJSON)
}

func (s *SmartContract) ReadStationData(ctx contractapi.TransactionContextInterface, id string, devicename string) (*StationData, error) {
	// cria a chave composta usando o id
	key, err := ctx.GetStub().CreateCompositeKey(compositeKey, []string{id, devicename})
	if err != nil {
		return nil, err
	}

	// buscar o valor associado à chave composta
	// *tentar usar getStateByPartialCompositeKey*
	value, err := ctx.GetStub().GetState(key)
	if err != nil {
		return nil, err
	}

	// verifique se o valor retornado é nulo
	if value == nil {
		return nil, fmt.Errorf("Nenhum valor encontrado para a chave %s", key)
	}

	// cria estrutura para receber manipular os dados recebidos
	var stationdata StationData

	// realiza o unmarshal dos dados recebidos na estrutura
	err = json.Unmarshal(value, &stationdata)
	if err != nil {
		return nil, err
	}

	return &stationdata, nil
}

// ReadAsset returns the asset stored in the world state with given id.
// func (s *SmartContract) ReadHCData(ctx contractapi.TransactionContextInterface, id string) ([]byte, error) {

// 	var results []interface{}

// 	resultsIterator, err := ctx.GetStub().GetStateByPartialCompositeKey(compositeKey, []string{id})

// 	if err != nil {
// 		return nil, err
// 	}

// 	defer resultsIterator.Close()

// 	for resultsIterator.HasNext() {
// 		kvResult, err := resultsIterator.Next()
// 		if err != nil {
// 			return nil, err
// 		}
// 		hcairtemperature := HCAirTemperature{}

// 		err = json.Unmarshal(kvResult.Value, &hcairtemperature)
// 		if err != nil {
// 			return nil, err
// 		}

// 		result := struct {
// 			HCKey          string `json:"hckey"`
// 			UpdateTimeUnix string `json:"updatetimeunix"`
// 		}{}

// 		prefix, keyParts, err := ctx.GetStub().SplitCompositeKey(kvResult.Key)
// 		if len(keyParts) < 2 {
// 			result.UpdateTimeUnix = prefix
// 		} else {
// 			result.HCKey = keyParts[0]
// 			result.UpdateTimeUnix = keyParts[1]
// 		}

// 		results = append(results, result)
// 	}

// 	hcairtemperatureJSON, err := json.Marshal(results)

// 	if err != nil {
// 		return nil, err
// 	}

// 	return hcairtemperatureJSON, err
// 	//return ctx.GetStub().Success(hcairtemperatureJSON)

// }
