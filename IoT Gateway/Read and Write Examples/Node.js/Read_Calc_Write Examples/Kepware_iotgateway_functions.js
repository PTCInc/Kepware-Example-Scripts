// -------------------------------------------------------------------------
// Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
// See License.txt in the project root for
// license information.
// --------------------------------------------------------------------------

// Provides generic functions used to interact with the IoT Gateway REST server interface.

//requires request module. Install with "npm install request"
const request = require('request'); 

//Kepware CRUD
module.exports.browseRestServer = function(username, pw, ip, port, callback) {
    var auth = 'Basic ' + Buffer.from(username + ':' + pw).toString('base64');
    request({
        url: 'http://' + ip + ':' + port + '/iotgateway/browse', //Refer to documentation of API under http://<IP:port>/iotgateway
        method: "GET",
        headers: {
            "content-type": "application/json",
            "Authorization": auth,
        },
    }, function(error, response, body) {
        if (error) {
            console.log("[ERROR] : " + error);
        };
        //console.log("[KEPWARE] : " + body);
        if (typeof(callback) === "function") {
            callback(body);
        }
    });
};

module.exports.readTags = function(username, pw, ip, port, tagArray, callback) { 
    //["Channel1.Device1.Tag1", "Channel1.Device1.Tag2"] - array example to read two tags
    var auth = 'Basic ' + Buffer.from(username + ':' + pw).toString('base64');
    request({
        url: 'http://' + ip + ':' + port + '/iotgateway/read',
        json: true,
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": auth,
        },
        json: tagArray,
    }, function(error, response, body) {
        if (error) {
            console.log("[ERROR] : " + error);
        };
        //console.log("[KEPWARE] : ");
        //console.log(body);
        if (typeof(callback) === "function") {
            callback(body);
        }
    });
};

module.exports.writeTags = function(username, pw, ip, port, tagArray, callback) { 
    //[{"id" : "Channel1.Device1.Tag1", "v": "Value to write"},{"id" : "Channel1.Device1.Tag2", "v": "Value to write"}]
    var auth = 'Basic ' + Buffer.from(username + ':' + pw).toString('base64');
    request({
        url: 'http://' + ip + ':' + port + '/iotgateway/write', //Requires explicit enabling during REST Server Set up
        json: true,
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": auth,
        },
        json: tagArray,
    }, function(error, response, body) {
        if (error) {
            console.log("[ERROR] : " + error);
        };
        //console.log("[KEPWARE] : ");
        //console.log(body);
        if (typeof(callback) === "function") {
            callback();
        }
    });
};

//Additional Functions
module.exports.getIoTServerTags = function(username, pw, ip, port, callback) {
    var auth = 'Basic ' + Buffer.from(username + ':' + pw).toString('base64');
    request({
        url: 'http://' + ip + ':' + port + '/iotgateway/browse', //Refer to documentation of API under http://<IP:port>/iotgateway
        method: "GET",
        headers: {
            "content-type": "application/json",
            "Authorization": auth,
        },
    }, function(error, response, body) {
        var tempObj = JSON.parse(body);
        var tempAry = [];
        for (var i = 0; i < tempObj['browseResults'].length; i++) {
            //console.log(tempObj['browseResults'][i]['id']);
            tempAry.push(tempObj['browseResults'][i]['id']);
        }
        if (error) {
            console.log("[ERROR] : " + error);
        };
        if (typeof(callback) === "function") {
            callback(tempAry);
        }
    });
};