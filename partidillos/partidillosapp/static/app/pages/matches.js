"use strict";   
define( ['text!templates/joined.template', 'db/restdb'], function ( joinedTmpl, database) {
  
  window.MyApp = Ember.Application.create({ });

  var MatchView = Ember.View.extend({
      template: Ember.Handlebars.compile(joinedTmpl),
      setMatches: function(matches){
          this.set('matches', matches);
          this.removeAndInsert();
      },
      removeAndInsert: function(){
          this.remove();
          this.appendTo(this.selector);
      }
  });



  function createMatchView(matches, title, selector, action){
        var view = MatchView.create({
            title: title,
            matches: matches,
            selector: selector,
            didInsertElement: function(){
                  $("#content").trigger('create'); 
            },
            matchClick: function(evt){
                var self = this;
                Ember.getPath(action).call(Ember.getPath('MyApp.controller'), evt.context.id);
            },
        });
        view.appendTo(selector);
        return view;
  }


  return { 
    init: function(){
      $.mobile.showPageLoadingMsg();
      var db = new database.DatabaseAccess();
      $.when(db.getJoined(), db.getPending()).then(function(joined, pending){
          MyApp.controller = Ember.Object.create({
              joinView : createMatchView(joined, "Voy a jugar", "#content", 'MyApp.controller.leaveMatch'),
              pendingView : createMatchView(pending, "Otros partidos", "#content", 'MyApp.controller.joinMatch'),
              joinMatch: function(id){
                  var self = this;
                  db.joinMatch("myplayer", id).done(this.update.call(this));
              },
              leaveMatch: function(id){
                  db.leaveMatch("myplayer", id).done(this.update.call(this));
              },
              update: function(){
                  var self = this;
                  $.mobile.showPageLoadingMsg();
                  $.when(db.getJoined(), db.getPending()).done(function(joined, pending){
                      self.joinView.setMatches(joined);
                      self.pendingView.setMatches(pending);
                      $.mobile.hidePageLoadingMsg();
                  });
              }


          }); 
          $.mobile.hidePageLoadingMsg();
      });

    }
  }
  
});
