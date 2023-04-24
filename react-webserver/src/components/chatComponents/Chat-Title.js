
import './Chat-Title.css';


function ChatTitle() {
    
    return (
        <div id="chat-title">
            <span>Nithesh Bonugu </span>
            <img src={require("../../images/trash-logo.svg").default} alt="Delete Conversation" />
        </div>
    );
}

export default ChatTitle;