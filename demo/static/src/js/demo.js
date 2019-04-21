/**
 * Created by baitao on 2017/3/7.
 */
/*
* 需要在odoo空间下创建新的模块function,这样framework才能找到fun，并进行初始化
* odoo.addonName
* instance:odoo web当前实例，提供odoo定义的功能，代码或其他模块定义的对象
* local:本地命名空间，从模块外部访问对象和变量或者odooweb需要调用的对象或者想自定义对象设置的地方
* 提供了一个虚拟类的实现，新建类Class需要通过继承odoo.web.Class()方式定义：var ClassName = instance.web.Class.extend({})
* 继承提供K,V的字典形式的类内容，可以声明一些方法或属性,属性可以通过this.XXX存储
* 方法中父类提供初始化方法供子类重写 init()->构造方法
* 新建的类也可以供其他类继承，使用extend方法,使用this._super()调用父类方法
* 可以通过new来实例化类
* widget
* 通过继承odoo.Widget.extend 重写start(自动调用的方法)等方法，末尾需要有一步注册通过odoo.web.client_actions.add
* $el可以在widget内使用，相当于jquery对象，默认$el相当于一个<div>元素
* */

// odoo.demo = function (instance,local) {
//     alert('demo');
//     // var _t = instance.web._t,
//     //     _lt = instance.web._lt;
//     // var QWeb = instance.web.qweb;
//    /* alert("demo test js");
//     local.test = "test";
//     var TestClass = instance.web.Class.extend({
//         init: function (name) {
//             this.name = name
//         },
//         say_hello: function () {
//             console.log("hello,testclass", this.name);
//         },
//     });
//     var test_object = new TestClass();
//     test_object.say_hello();
//     test_object.name = "Test-name";
//     test_object.say_hello();
//     var test1_object = new TestClass("Test1-name");
//     test1_object.say_hello();*/
//     //widget
//     local.HomePage = instance.Widget.extend({
//         start: function () {
//             console.log("demo homepage widget");
//             this.$el.append("<div>homepage widget</div>");
//         },
//     });
//     //注册
//     instance.web.client_actions.add('demo.homepage', 'instance.demo.HomePage');
// };
odoo.define('demo.home_page', function (require) {
    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var data = require('web.data');

    var QWeb = core.qweb;
    var _t = core._t;
    /**
     * template：使用qweb模板，模板以根节点形式append到页面中，start中的dom为模板的子节点
     * 模板<div>xxxx<DIV>homepage widget ...</DIV></div>,当模板中存在两个非t标签的dom时，widgetstart内容都会添加到
     * 多个dom内，但是start拼接的第二个widget只有一个div内添加了
     * ？关联模板之后，widget的根div的class没了
     * this.$el.append(QWeb.render("HomePageTemplate"));也可以渲染模板
     * qweb可以调用widget中的数据
     * this.trigger('event_name', argument1,argument2,...) trigger第一个参数必须为事件名，供监听器方法监听
     * 可以用on监听该事件，如有a widget（在按钮点击时调用trigger）
     * 使用a的实例on方法 a_widget.on("event_name", this, this.user_chose);
     * trigger的后续参数(argument1,argument2,...),可以作为参数传入on的触发fun中 fun(argument1,argument2,...)
     * this.set("", "")set可以给当前widget赋一些属性，可使用this.get("")调用属性值
     * on第一个参数可以携带属性名"eventName:propertiesName" 双向绑定联动么？
     */
    var HomePage = Widget.extend({
        template: "HomePageTemplate",
        className: 'oe_demo_homepage',
        /*events: {
            "click .my_button": "button_clicked",
        },
        button_clicked: function () {
            //event func
        },*/
        init: function (parent) {
            this._super(parent);
            this.name = "NameTest";
        },
        start: function () {
            var self = this;
            console.log("demo homepage widget");
            self.$el.append("<div>homepage widget</div>");
            var greeting = new GreetingsApendTo(this);
            greeting.appendTo(this.$el);
            //jquery selector widget提供find方法获取dom元素this.$el.find("input.my_input")...
            //也可以直接用$()，this.$("input.my_input")...,这个由于是在root范围内取，所以可能或取错dom，建议范围小用
            //console.log("test class---------->" + this.$el.find("div.test").text());
            //取到dom后，可以直接使用jquery事件触发函数，如.click() .change()等
            //使用问题
            // 1,冗长2,不支持运行时替换widget根元素，绑定只能在start中进行（widget初始化）3,需要解决this作用域绑定问题
           /* this.$(".my_button").click(function() {
                self.button_clicked();
            });*/
            //widget提供events对象,类似键值对的声明,键为 "动作 选择器" 值为"funName"触发的方法名,
            // 不加选择器，对应触发该widget的事件，这种方式this指向该widget的实例
            //从持久层取值
            // 取model的_name通过new一个Model对象
            //取model的传参方法，
            // 通过call(method_name,[arg1,arg2...],{a: arg1,b:arg2...})方法，参数数组/map 为model的方法传参
            // model的传参方法需要用api装饰器Model
            var demoProjectModel = new Model('demo.project');
            demoProjectModel.call("model_method",{context: new data.CompoundContext({'new_key':'key_value'})})
                .then(function (result) {
                self.$el.append("<div class='model_method'>Hello " + result["keyName"] + "</div>");
            });
            /*demoProjectModel.call("search",[],{limit: 15})
                .then(function (ids) {
                    return demoProjectModel.call('read',[ids,['name', 'no']]);
                })
                .then(function (users) {
                    //处理users的数据
                });*/
            //上面方法等同于使用query方法
           /* demoProjectModel.query(['name','no'])
                .filter([])
                .limit(15)
                .all().then(function (users) {
                    //处理users的数据

            });*/
        },
    });
    var GreetingsApendTo = Widget.extend({
        className: 'oe_demo_greeting',
        init: function (parent) {
          this._super(parent);
        },
        start: function () {
            this.$el.append("<div class='test'>Test append to</div>")
        },
    });
    core.action_registry.add('demo_home_page', HomePage);
    return HomePage;
});

