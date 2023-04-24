

import './Message-List.css';

function MessageList() {
    return (
        <div id="chat-message-list">
            <div className="message-row you-message">
                <div className="message-content">
                    <div className="message-text">Oh okay</div>
                    <div className="message-time">Apr 16</div>
                </div>
            </div>
            <div className="message-row other-message">
                <div className="message-content">
                    <img src={require("../../images/blank.jpeg")} width="50" height="50" alt="Daryl Duckmanton" />
                    <div className="message-text">
                        **THE NUMBER YOU'RE TRYING TO REACH IS INVALID**
                    </div>
                    <div className="message-time">Apr 16</div>
                </div>
            </div>
            <div className="message-row you-message">
                <div className="message-content">
                    <div className="message-text">
                        What?
                    </div>
                    <div className="message-time">Apr 15</div>
                </div>
            </div>
            <div className="message-row other-message">
                <div className="message-content">
                    <img src={require("../../images/blank.jpeg")} width="50" height="50" alt="Daryl Duckmanton" />
                    <div className="message-text">
                        Hello? HELOOOO? Sorry, I can't hear you. 
                        TTYL
                    </div>
                    <div className="message-time">Apr 16</div>
                </div>
            </div>
            <div className="message-row you-message">
                <div className="message-content">
                    <div className="message-text">
                        Well we need to talk about the money you owe me. I need it and it is urgent
                    </div>
                    <div className="message-time">Apr 15</div>
                </div>
            </div>
            <div className="message-row other-message">
                <div className="message-content">
                    <img src={require("../../images/blank.jpeg")} width="50" height="50" alt="Daryl Duckmanton" />
                    <div className="message-text">
                        I'm just trying to figure out this moderating
                        systems lab
                    </div>
                    <div className="message-time">Apr 14</div>
                </div>
            </div>
            <div className="message-row you-message">
                <div className="message-content">
                    <div className="message-text">
                        How's it going?
                    </div>
                    <div className="message-time">Apr 13</div>
                </div>
            </div>
            <div className="message-row other-message">
                <div className="message-content">
                    <img src={require("../../images/blank.jpeg")} width="50" height="50" alt="Daryl Duckmanton" />
                    <div className="message-text">
                        Hey mate what's up?
                    </div>
                    <div className="message-time">Apr 13</div>
                </div>
            </div>
            <div className="message-row you-message">
                <div className="message-content">
                    <div className="message-text">
                        Ayo
                    </div>
                    <div className="message-time">Apr 13</div>
                </div>
            </div>
        </div>
    );
}

export default MessageList;