/**
 * mvc.js
 * @author: Marko Čibej
 * @description: mvc framework based on simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/


/**
 * Simple MVC, 2016 Todd Zebert
 * Event Listeners and notifications module
 */
var mvc = (function mvc(simple) {
  'use strict';

  // sender is the context of the Model or View which originates the event
  simple.Event = function SimpleEvent(sender) {
    this.sender = sender;
    this.listeners = [];
  };

  simple.Event.prototype = {
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

  return simple;
})(mvc || {});


/**
 * A 1-way View Module
 */
var mvc = (function mvc(simple) { // eslint-disable-line no-redeclare, no-shadow
  'use strict';

  simple.OneWayView = function simpleOneWayView(model, selector) {

    this._model = model;
    this._selector = selector;

    // since not a 2-way, don't need to set this.onChanged

    // attach model listeners
    this._model.onSet.attach(
      () => this.show()
    );

  };

  simple.OneWayView.prototype = {
    show() {
      this._selector.innerHTML = this._model.get();
    },
  };

  return simple;
})(mvc || {}); // eslint-disable-line no-use-before-define, no-redeclare, no-shadow


/**
 * A 2-way View Module
 */
var mvc = (function mvc(simple) { // eslint-disable-line no-redeclare, no-shadow
  'use strict';

  // selector is a DOM element that supports .onChanged and .value
  simple.TwoWayView = function simpleTwoWayView(model, selector) {

    this._model = model;
    this._selector = selector;

    // for 2-way binding
    this.onChanged = new simple.Event(this);

    // attach model listeners
    this._model.onSet.attach(
      () => this.show()
    );

    // attach change listener for two-way binding
    this._selector.addEventListener("change",
      e => this.onChanged.notify(e.target.value)
    );

  };

  simple.TwoWayView.prototype = {
    show() {
      this._selector.value = this._model.get();
    },
  };

  return simple;
})(mvc || {}); // eslint-disable-line no-use-before-define, no-redeclare, no-shadow


/**
 * Controller module
 */
var mvc = (function mvc(simple) { // eslint-disable-line no-redeclare, no-shadow
  'use strict';

  simple.Controller = function SimpleController(model, view) {

    this.model = model;
    this.view = view;

    if (this.view.hasOwnProperty('onChanged')) {
      this.view.onChanged.attach(
        (sender, data) => this.update(data)
      );
    }
  };

  simple.Controller.prototype = {
    update(data) {
      this.model.set(data);
    },
  };

  return simple;
})(mvc || {}); // eslint-disable-line no-use-before-define, no-redeclare, no-shadow


/**
 * main
 *
 * for demonstration
 */
var main = function() {
  var model = new mvc.Model(12), // 12 is initial value

    aView = new mvc.TwoWayView(model, document.getElementById('points-a')),
    aController = new mvc.Controller(model, aView), // eslint-disable-line no-unused-vars

    bView = new mvc.OneWayView(model, document.getElementById('points-b')),
    bController = new mvc.Controller(model, bView); // eslint-disable-line no-unused-vars

  // these are for initial show, if not shown some other way
  aView.show();
  bView.show();

  // example of changing the model directly
  window.setTimeout(
    () => model.set(20),
    4000
  );

};

document.addEventListener('DOMContentLoaded', main, false);