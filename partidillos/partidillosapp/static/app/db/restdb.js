

define([], function(){

    function DatabaseAccess(){
    }
        

    DatabaseAccess.prototype.getJoined = function(){
        return $.get("/partidillos/api/matches/joined/").pipe(function(data){
            return data;
        });
    };

    DatabaseAccess.prototype.getPending = function (){ 
        return $.get("/partidillos/api/matches/pending/").pipe(function(data){
            return data;
        });
    };

    DatabaseAccess.prototype.joinMatch = function (player, matchId){ 
        var url = "/partidillos/api/matches/" + matchId + "/join/"
        return $.get(url);
    };

    DatabaseAccess.prototype.leaveMatch = function (player, matchId){ 
        var url = "/partidillos/api/matches/" + matchId + "/leave/"
        return $.get(url);
    };

    return {
        DatabaseAccess: DatabaseAccess
    }


});
