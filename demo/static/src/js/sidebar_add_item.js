/**
 * Created by baitao on 2017/3/27.
 */
odoo.define('demo.sidebar_add_item', function (require) {
    var core = require('web.core');
    var data = require('web.data');
    var Dialog = require('web.Dialog');

    var _t = core._t;
    var QWeb = core.qweb;
    var ListView = require('web.ListView');
    var Sidebar = require('web.Sidebar');
    //var ProjectExport = require('demo.projectExport');
   /* Sidebar.include({
        start: function () {
            var self = this;
            this._super(this);
            var view = this.getParent();
            console.log("view type----->" + view.fields_view.type);//tree form
            self.add_items('other',[
                {
                    label:_t('test'),
                    callback: self.on_click_test,
                },
            ]);
        },
        on_click_test: function (item) {
            var view = this.getParent();
            console.log('click---->',view);
            console.log(view.groups.get_selection().ids);//array
            new ProjectExport(this, view.groups.get_selection().ids).open();
        },
    });*/
   /*ListView.include({
        render_sidebar: function($node) {
             if (!this.sidebar && this.options.sidebar) {
                this.sidebar = new Sidebar(this, {editable: this.is_action_enabled('edit')});
                if (this.fields_view.toolbar) {
                    this.sidebar.add_toolbar(this.fields_view.toolbar);
                }
                this.sidebar.add_items('other', _.compact([
                    { label: _t("Export"), callback: this.on_sidebar_export },
                    { label: _t("test"), callback: this.on_click_test },
                    this.fields_view.fields.active && {label: _t("Archive"), callback: this.do_archive_selected},
                    this.fields_view.fields.active && {label: _t("Unarchive"), callback: this.do_unarchive_selected},
                    this.is_action_enabled('delete') && { label: _t('Delete'), callback: this.do_delete_selected }
                ]));

                $node = $node || this.options.$sidebar;
                this.sidebar.appendTo($node);

                // Hide the sidebar by default (it will be shown as soon as a record is selected)
                this.sidebar.do_hide();
            }
        },
        on_click_test: function () {
            var ids = this.groups.get_selection().ids;
            console.log("ids----->" + ids);
        }
    });*/
});