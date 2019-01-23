/**
 * main.js
 * @author: Marko Čibej
 * @description: the entry point, triggered from jQuery's document.ready()
 * inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/

var main = function() {
  var worksModel = new mvc.Works();
  var cardView = new mvc.Cards(worksModel, $('#full-deck'));
  var cardController = new mvc.CardDealer(worksModel, cardView);

  worksModel.reload();
};

$(document).ready(main);
