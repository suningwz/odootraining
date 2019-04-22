//首先通过odoo.define("namespaceName",function(require){});声明当前作用域适用范围
odoo.define('oepetstore.petstore', function (require) {   //第一个参数为"模块名.js文件名",第二个参数为一个函数
"use strict";
    //通过require引入要使用的js模块
    var Class = require('web.Class');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var utils = require('web.utils');
    var _t = core._t;
    var _lt = core._lt;
    
    //创建Widget  
    //主要属性有className--widget创建的dom元素的class，events--widget的事件表，temlate--widget的qweb模板
    //主要方法有init--初始化实例的方法，start--widget自动调用的方法
    var homePage = Widget.extend({
        init: function(parent) {
            this._super(parent);
            console.log("Hello JS, I'm inside of init.");
        },
        start: function() {
            console.log("Your pet store home page loaded");
        },
    });
    //将homePage注册到action，并取名为'petstore'，在ir.actions.client动作里的tag标签，使用的是'petstore'。而不是homePage
    core.action_registry.add('petstore', homePage);  
    return homePage;

});