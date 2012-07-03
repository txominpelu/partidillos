
define([], function(){

    function DatabaseAccess(){
        this.joined = [
            {
              "id" : "1",
              "date": "12:20",
              "place" : "place_joined"
            },
            {
              "id" : "3",
              "date": "15:20",
              "place" : "place_joined2"
            }
        ];
        this.pending = [
            {
              "id" : "2",
              "date": "12:20",
                  "place" : "place_pending"
                }
            ];
    }
        

    DatabaseAccess.prototype.getJoined = function(){
        var dfd = $.Deferred();
        dfd.resolve( this.joined );
        return dfd.promise();
    };

    DatabaseAccess.prototype.getPending = function (){ 
        var dfd = $.Deferred();
        dfd.resolve( this.pending );
        return dfd.promise();
    };

    DatabaseAccess.prototype.joinMatch = function (player, matchId){ 
        var dfd = $.Deferred();
        var joinedMatch = this.pending.filter(function(match){
            return match.id === matchId;
        })[0];
        this.pending = this.pending.filter(function(match){
            return match.id !== matchId;
        });
        this.joined.push(joinedMatch);
        dfd.resolve( );
        return dfd.promise();
    };

    DatabaseAccess.prototype.leaveMatch = function (player, matchId){ 
        var dfd = $.Deferred();
        var leftMatch = this.joined.filter(function(match){
            return match.id === matchId;
        })[0];
        this.joined = this.joined.filter(function(match){
            return match.id !== matchId;
        });
        this.pending.push(leftMatch);
        dfd.resolve( );
        return dfd.promise();
    };

    return {
        DatabaseAccess: DatabaseAccess
    }


});
