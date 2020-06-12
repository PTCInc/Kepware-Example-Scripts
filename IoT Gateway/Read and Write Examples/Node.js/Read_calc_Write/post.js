// -------------------------------------------------------------------------
// Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
// See License.txt in the project root for
// license information.
// --------------------------------------------------------------------------

var request = require('request');

exports.writerequest = function(requestData) {
    request({
        url: 'http://localhost:39320/iotgateway/write',
        method: "POST",
        json: true,
        headers: {
            "content-type": "application/json",
        },
        json: requestData
    }, function(error, response, body) {
        console.log('write sucessful');
    })
}