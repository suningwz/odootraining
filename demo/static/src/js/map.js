/**
 * Created by baitao on 2017/3/9.
 */
odoo.define('demo.map', function (require) {
    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var data = require('web.data');

    var QWeb = core.qweb;
    var _t = core._t;
    var BaiduMap = Widget.extend({
        template: "BaiduMap",
        events: {
            "click .my_button": "button_clicked",
        },
        button_clicked: function () {
            //event func
            var demoProjectModel = new Model('demo.project');
            demoProjectModel.call("model_method",{context: new data.CompoundContext({'new_key':'key_value','record_id': this.recordId,})})
                .then(function (result) {
                alert(result["keyName"]);
            });
        },
        init: function (parent, context) {
            this._super(parent);
            this.testValue = 'value';
            this.recordId = null;
            if (context && context.context && context.context.record_id) {
                this.recordId = context.context.record_id;
            }
            //alert(context.context.record_id);
        },
        start: function () {
            var self = this;
            console.log("demo baidumap widget");
            var src = "/baidu_map/?width=898&height=485&testValue=" + this.testValue;
            console.log(this.$el.find("iframe.iMap").attr("style"));
            this.$el.find("iframe.iMap").attr("src", src);
            //获取iframe内dom,等待ifram内容渲染
            //setTimeout(alert(this.$(this.$el.find("iframe.iMap").document).find('div.x').text()),5000);

        },
    });

    core.action_registry.add('demo_baidu_map', BaiduMap);
    return BaiduMap;
});