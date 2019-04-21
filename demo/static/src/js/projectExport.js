/**
 * Created by Administrator on 2017/3/27.
 */
odoo.define('demo.projectExport', function (require) {
    var core = require('web.core');
    var crash_manager = require('web.crash_manager');
    var data = require('web.data');
    var Dialog = require('web.Dialog');
    var framework = require('web.framework');
    var pyeval = require('web.pyeval');

    var QWeb = core.qweb;
    var _t = core._t;
    var ProjectExport = Dialog.extend({
        init: function(parent, ids) {
            var options = {
                title: _t("Export Data"),
                buttons: [
                    {text: _t("Export To File"), click: this.export_data, classes: "btn-primary"},
                    {text: _t("Close"), close: true},
                ],
            };
            this._super(parent, options);
            this.records = {};
            //this.dataset = dataset;
            //this.exports = new data.DataSetSearch(this, 'ir.exports', this.dataset.get_context());
            this.ids = ids;

            this.row_index = 0;
            this.row_index_level = 0;
        },
        start: function () {

        },
        export_data: function () {
            console.log("export");
            console.log(this.ids);
        }
    });
    return ProjectExport;
});