// XXX: uses chatapp.html template!

var ChatView = Backbone.View.extend({
	className: 'chatView',

	// Subviews 
	views: {
		chatWindow: null,
		input: null,
	},
	
	initialize: function() {
		// Static render
		this.$el = $('.'+this.className)
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE')
					.appendTo('#attach');

		this.show();

		// Subviews
		var chatwin = new ChatWindowView();
		var input = new InputView();

		this.$el.find('.chatWindowContainer')
			.html(chatwin.$el);

		this.$el.find('.inputContainer')
			.html(input.$el);

		this.views.chatWindow = chatwin;
		this.views.input = input;

		// Events
		this.listenTo(this.model, 'change', this.render);
	},

	render: function() {
		// TODO
		this.$el.find('.chatName').html(this.model.getName());
	},

	show: function() { 
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});

var ChatApp = Backbone.View.extend({
	//chats: [],

	initialize: function() {

		var chat = new Chat({id: 6});
		var chatView = new ChatView({model:chat});

		chat.fetch({
			success: function(m) {
				console.log(m.get('issue'));
			}
		});

	},
});

