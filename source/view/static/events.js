/**
 * events.js
 * @author: Marko Čibej
 * @description: a trivial event handling framework
 * inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/

var mvc = (function mvc(self) {
  'use strict';

  // sender is the context of the Model or View which originates the event
  self.Event = function SimpleEvent(sender) {
    this.sender = sender;
    this.listeners = [];
  };

  self.Event.prototype = {
    // add listener closures to the list
    attach(listener) {
      this.listeners.push(listener);
    },
    // loop through, calling attached listeners
    notify(args) { this.listeners.forEach(
      (v, i) => this.listeners[i](this.sender, args)
      )
    },
  };

  return self;
})(mvc || {});