// -------------------------------------------------------------------------
// Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
// See License.txt in the project root for
// license information.
// --------------------------------------------------------------------------

//=====================================================
//Description: This app issues a HTTP GET from a third party API, flattens the structure and loads the data into Kepware via HTTP Post to a REST Server in IoT Gateway
//1. Get the data from endpoint
//2. Take the data and extract only the data
//3. From observation of sample, index 0 is the latest
//4. Break object in index 0 and write to Kepware
//5. Repeat at desired sampling rate
//=====================================================


var request = require('request');
const kepwareIotGateway = require('../Kepware_iotgateway_functions');
var kseIp = '127.0.0.1';
var iotGatewayPort = 39320;

//Make use of Security Policies and User manager to enhance security
var user = 'Administrator'; 
var pw = '';

var samplingRate = 5000; //5 seconds
var ChannelDeviceString = 'bom_gov.json.';
var timeNow = Date.now();

var options = {
    url: 'http://www.bom.gov.au/fwo/IDN60901/IDN60901.94767.json',
    'keepAlive': 'true',
    headers: {
        'User-Agent': 'request'
    }
}

getBomData = function() { 
    //1. Get the data from endpoint
    request.get(options, function(error, response, body) {
        console.log(body);
        var objTemp = JSON.parse(body);
        //2. Take the data and extract only the data && 3. From observation of sample, index 0 is the latest
        var latestObjData = objTemp["observations"]["data"][0]; 
        console.log(JSON.stringify(latestObjData));
        //4. Break object in index 0 and write to Kepware
        var jsonArray = returnArray(latestObjData); 
        console.log(jsonArray); //output it 
        kepwareIotGateway.writeTags(user, pw, kseIp, iotGatewayPort, jsonArray);

    })
};

returnArray = function(jsonData) {
    //Takes obj and returns the an array of JSONS required by Kepware
    // [{ "id": "Channel1.Device1.tag1", "v": 42 }]
    var jsonKeys = Object.keys(jsonData);
    var maxKey = jsonKeys.length;
    var string;
    var arry = [];
    for (var i = 0; i < maxKey; i++) {
        string = "" + '{"id" : "' + ChannelDeviceString + jsonKeys[i] + '", "v" : "' + jsonData[jsonKeys[i]] + '" }';
        arry.push(JSON.parse(string));
    }
    return arry;

}

getBomData();
setInterval(function() {
    getBomData();
}, samplingRate); //5. Repeat at desired sampling rate