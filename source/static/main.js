/**
 * main.js
 * @author: Marko Čibej
 * @description: the entry point, triggered from jQuery's document.ready()
 * inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/

var main = function() {
  var cardView = new writing.CardsView($('#full-deck'));

  worksAdapter.reload();
};

$(document).ready(main);
