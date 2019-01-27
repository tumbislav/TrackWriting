/**
 * events.js
 * @author: Marko Čibej
 * @description: a trivial event handling framework for the trackWriting application
 */


var writing = (function writing(self) {
  'use strict';

  // an event has a sender and listeners
  self.Event = function(sender) {
    this.sender = sender;
    this.listeners = [];
  };

  self.Event.prototype = {

    // attaching a listener is simply adding it to the list
    attach(listener) {
      this.listeners.push(listener);
    },

    // loop through the attached listeners and call each one in turn
    notify(args) {
      this.listeners.forEach(
        (listener) => listener(this.sender, args)
      )
    },
  };

  return self;
})(writing || {});