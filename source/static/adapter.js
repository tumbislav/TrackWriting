/**
 * adapter.js
 * @author: Marko Čibej
 * @description: the adapter part of the application, responsible for communicating with the model
 *    that is defined by the REST API, and the controller that is model-agnostic.
 *    The application is enclosed in the 'writing' namespace.
 */

/**
 * The entire application is packaged in the 'writing' namespace.
 */
var writing = (function writing(self, $) {
    'use strict';

    self.Works = function (view) {
        // the model's data cache
        this.works = null;
        this.classifiers = null;
        this.translations = null;
        // the configuration
        this.preferred_language = 'en';
        this.current_translation = null;

        // Events we generate ourselves.
        // initial load or reload
        this.onReload = new self.Event(this);
        this.onError = new self.Event(this);
    };

    // the main functionality
    self.Works.prototype = {

        import() {
            $.ajax({
                context: this,
                type: 'GET',
                url: '/import',
                success: function(data, status, xhr) {
                    this.reload();
                },
                error: function(xhr, status, error) {
                    let details = JSON.parse(xhr.responseText);
                    this.onError.notify(error + ': ' + details['error']);
                }
            });
        },

        attachView(view) {
            // adding a new work
            if (view.hasOwnProperty('onAdd')) {
                view.onAdd.attach((sender, data) => this.addWork(data));
            }
            // deleting a work
            if (view.hasOwnProperty('onDelete')) {
                view.onDelete.attach((sender, data) => this.deleteWork(data));
            }
            // changing an existing work
            if (view.hasOwnProperty('onUpdate')) {
                view.onUpdate.attach((sender, data) => this.updateWork(data));
            }
        },

        // clear current data and reload everything from server, then tell the views to refresh
        reload() {
            let _this = this;
            $.when(
                $.get('/works', function (data, status, xhr) {
                    if (status == 'success') {
                        _this.works = data;
                    }
                    else {
                        _this.onError.notify('GET /works '); // + xhr.statusText)
                    }
                }, 'json'),
                $.get('/classifiers', function (data, status, xhr) {
                    if (status == 'success') {
                        _this.classifiers = data;
                    }
                    else {
                        _this.onError.notify('GET /classifiers '); //  + xhr.statusText)
                    }
                }, 'json'),
                $.get('/translations', function (data, status, xhr) {
                    if (status == 'success') {
                        _this.translations = data;
                        _this.prepareTranslation();

                    }
                    else {
                        _this.onError.notify('GET /translations '); //  + xhr.statusText)
                    }
                }, 'json')
            ).then(function () {
                _this.onReload.notify();
            });
        },

        prepareTranslation() {
            if (this.preferred_language != null &&
                    this.translations.hasOwnProperty(this.preferred_language)) {
                this.current_translation = this.translations[this.preferred_language];
            }
        },

        translationContext(context) {
            return (this.current_translation.hasOwnProperty(context) ? this.current_translation[context] : {});
        },

        translateString(context, value) {
            let ctx = this.translationContext(context);
            return (ctx.hasOwnProperty(value) ? ctx[value] : value);
        },

        translateList(context, values) {
            let ctx = this.translationContext(context);
            return values.map((value) => (ctx.hasOwnProperty(value) ? ctx[value] : value))
        },

        translateWork(work) {
            let adapted = {};
            adapted.code = work.code;
            adapted.type = work.type;
            adapted.name = work.name;
            adapted.world = work.world;
            adapted.series = work.series;
            adapted.genre = this.translateString('genres', work.genre);
            adapted.form = work.form;
            adapted.status = work.status;
            adapted.word_count = work.word_count;
            return adapted;
        },

        // get the simple version of the works list
        getWorks() {
            let work_list = [];
            for (let[n, work]of this.works.entries()) {
                work_list.push(this.translateWork(work));
            }
            return work_list;
        },

        // add a work and notify listeners
        addWork(work) {
            $.noop();
        },
        deleteWork(work) {
            $.noop();
        },
        updateWork(work) {
            $.ajax({
                url: '/works',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(work)
            });
        },
    };

    return self;
})(writing || {}, jQuery);
