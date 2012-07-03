var jam = {
    "packages": [
        {
            "name": "jquery",
            "location": "jam/jquery",
            "main": "jquery.js"
        },
        {
            "name": "ember",
            "location": "jam/ember",
            "main": "ember-0.9.8.1.js"
        }
    ],
    "version": "0.1.9",
    "shim": {
        'ember': { 
            "deps": ['jquery'], 
            "exports": 'Ember' 
        } 
    }
};


if (typeof require !== "undefined" && require.config) {
    require.config({packages: jam.packages, shim: jam.shim});
    require.config({"baseUrl": "/static/app/"});
}
else {
    var require = {packages: jam.packages, shim: jam.shim};
}


if (typeof exports !== "undefined" && typeof module !== "undefined") {
    module.exports = jam;
};
