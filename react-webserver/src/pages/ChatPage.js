
import ConversationList from '../components/chatComponents/Conversation-List';
import NewConversation from '../components/chatComponents/New-Conversation';
import ChatTitle from '../components/chatComponents/Chat-Title';
import MessageList from '../components/chatComponents/Message-List';
import ChatForm from '../components/chatComponents/Chat-Form';

import '../components/chatComponents/Chat-Shell.css';

function ChatShell() {
    return (
        <div id="chat-container">
            <ConversationList />
            <NewConversation />
            <ChatTitle />
            <MessageList />
            <ChatForm />
        </div>
    );

}

export default ChatShell;