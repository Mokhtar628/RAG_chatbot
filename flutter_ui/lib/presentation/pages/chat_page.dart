import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/chat_bloc.dart';
import '../bloc/chat_event.dart';
import '../bloc/chat_state.dart';
import '../../domain/entities/chat.dart';
import '../widgets/bubble_clipper.dart';

class ChatPage extends StatefulWidget {
  const ChatPage({Key? key}) : super(key: key);

  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isNotEmpty) {
      // Dispatch the event to send a message.
      BlocProvider.of<ChatBloc>(context).add(SendMessageEvent(text));
      _controller.clear();
      _scrollToBottom();
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 300), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  // Build a chat bubble with a custom clip path.
  Widget _buildChatBubble(Chat chat, bool isUser) {
    if (isUser) {
      return Align(
        alignment: Alignment.centerRight,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
          padding: const EdgeInsets.all(12),
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.75,
          ),
          decoration: BoxDecoration(
            color: Colors.pinkAccent,
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(16),
              bottomLeft: Radius.circular(16),
              bottomRight: Radius.circular(16),
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.1),
                blurRadius: 4,
                offset: Offset(2, 2),
              ),
            ],
            gradient: LinearGradient(
              colors: [Colors.pinkAccent, Colors.pinkAccent.shade700],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
          child: Stack(
            children: [
              // Tail for the user's chat bubble
              Positioned(
                right: -10,
                bottom: 0,
                child: ClipPath(
                  clipper: ChatBubbleTailClipper(isUser: true),
                  child: Container(
                    width: 20,
                    height: 20,
                    color: Colors.pinkAccent,
                  ),
                ),
              ),
              Text(
                chat.question,
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
            ],
          ),
        ),
      );
    } else {
      // For bot messages: display a robot icon beside the bubble.
      Widget content;
      if (chat.answer == 'typing') {
        // Show an animated three-dot typing indicator.
        content = const TypingIndicator();
      } else {
        content = Text(
          chat.answer,
          style: const TextStyle(color: Colors.black87, fontSize: 16),
        );
      }

      return Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Padding(
            padding: const EdgeInsets.all(6.0),
            child: Image.asset(
              'assets/chat_logo.png',
              width: 70,
              height: 70,
            ),
          ),
          Flexible(
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 4),
              padding: const EdgeInsets.all(12),
              constraints: BoxConstraints(
                maxWidth: MediaQuery.of(context).size.width * 0.75,
              ),
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.only(
                  topRight: Radius.circular(16),
                  bottomLeft: Radius.circular(16),
                  bottomRight: Radius.circular(16),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 4,
                    offset: Offset(2, 2),
                  ),
                ],
                gradient: LinearGradient(
                  colors: [Colors.grey.shade300, Colors.grey.shade400],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              child: Stack(
                children: [
                  // Tail for the bot's chat bubble
                  Positioned(
                    left: -10,
                    bottom: 0,
                    child: ClipPath(
                      clipper: ChatBubbleTailClipper(isUser: false),
                      child: Container(
                        width: 20,
                        height: 20,
                        color: Colors.grey.shade300,
                      ),
                    ),
                  ),
                  content,
                ],
              ),
            ),
          ),
        ],
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('RAG Chat Bot'),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Chat messages list.
            Expanded(
              child: BlocConsumer<ChatBloc, ChatState>(
                listener: (context, state) {
                  // Optionally show error messages as SnackBars.
                  if (state is ChatError) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(state.message)),
                    );
                  }
                },
                builder: (context, state) {
                  List<Chat> chats = [];
                  if (state is ChatLoaded) {
                    chats = state.chats;
                  }
                  return ListView.builder(
                    controller: _scrollController,
                    itemCount: chats.length,
                    itemBuilder: (context, index) {
                      final chat = chats[index];
                      // If answer is empty, it's a user message.
                      final isUser = chat.answer.isEmpty;
                      return _buildChatBubble(chat, isUser);
                    },
                  );
                },
              ),
            ),
            // Input field and send button.
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(15)),
                  color: Colors.grey.shade200,
                ),
                padding:
                const EdgeInsets.symmetric(horizontal: 25, vertical: 8),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _controller,
                        textCapitalization: TextCapitalization.sentences,
                        decoration: const InputDecoration.collapsed(
                          hintText: 'Ask obout our policy...',
                        ),
                        onSubmitted: (_) => _sendMessage(),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.send_rounded, color: Colors.pinkAccent),
                      onPressed: _sendMessage,
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// A custom widget that animates three dots (simulating “typing…”).
class TypingIndicator extends StatefulWidget {
  const TypingIndicator({Key? key}) : super(key: key);

  @override
  _TypingIndicatorState createState() => _TypingIndicatorState();
}

class _TypingIndicatorState extends State<TypingIndicator> {
  int _dotCount = 1;
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    // Update the dot count every 500ms.
    _timer = Timer.periodic(const Duration(milliseconds: 500), (timer) {
      setState(() {
        _dotCount = (_dotCount % 3) + 1;
      });
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    String dots = '.' * _dotCount;
    return Text(
      dots,
      style: const TextStyle(fontSize: 20, color: Colors.black87),
    );
  }
}
