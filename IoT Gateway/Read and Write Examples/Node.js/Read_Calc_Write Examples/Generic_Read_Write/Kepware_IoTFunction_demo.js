// -------------------------------------------------------------------------
// Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
// See License.txt in the project root for
// license information.
// --------------------------------------------------------------------------
//IoT Gateway Functions Demo - NodeJS
const kepwareIotGateway = require('../Kepware_iotgateway_functions');

//Config Param
var kseIp = '127.0.0.1';
var iotGatewayPort = 39320;
//Make use of Security Policies and User manager to enhance security
var user = 'Administrator'; 
var pw = '';

//--------------INITIALIZATION--------------//

//Browse the server and ETL the returned json for reading latere
//Standard browse
kepwareIotGateway.browseRestServer(user, pw, kseIp, iotGatewayPort, (data) => console.log('[Browse JSON Return] : ' + data + '\n')); 
//Gets listing of items and executes a read of the list of items
kepwareIotGateway.getIoTServerTags(user, pw, kseIp, iotGatewayPort, function(data) { 
    console.log('[Reformed in browse REST Server] : ' + data + '\n'); 
    var readAry = data;
    kepwareIotGateway.readTags(user, pw, kseIp, iotGatewayPort, readAry, (data) => console.log('[Read JSON Return] : ' 
        + JSON.stringify(data)));
});

//Writes unix timestamp to Tag "bom_gov.scriptwriteback.timestamp_last" - Could be used as a heartbeat signal
kepwareIotGateway.writeTags(user, pw, kseIp, iotGatewayPort, [{ "id": "bom_gov.scriptwriteback.timestamp_last", "v": Date.now() }]);