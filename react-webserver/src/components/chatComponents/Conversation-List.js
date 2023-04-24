
import './Conversation-List.css';


function ConversationList() {
    
    return (
        <div id="conversation-list">
                <div className="conversation active">
                    <img src={require("../../images/blank.jpeg")} alt="Daryl Duckmanton" />
                    <div className="title-text">Nithesh Bonugu</div>
                    <div className="created-date">Apr 16</div>
                    <div className="conversation-message"> 
                        Aight, I'm out
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Kim O'Neil" />
                    <div className="title-text">Tim Tardashian</div>
                    <div className="created-date">2 days ago</div>
                    <div className="conversation-message">
                        I painted on a banana
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="John Anderson" />
                    <div className="title-text">Brake</div>
                    <div className="created-date">1 week ago</div>
                    <div className="conversation-message">
                        I need a one dance
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Ben Smith" />
                    <div className="title-text">Ellie Bilish</div>
                    <div className="created-date">2:49 PM</div>
                    <div className="conversation-message">
                        I'm dying my hair yellow next
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Douglas Johannasen" />
                    <div className="title-text">Melon Tusk</div>
                    <div className="created-date">6:14 PM</div>
                    <div className="conversation-message">
                        Chesla is not going to Tars
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Jacob Manly" />
                    <div className="title-text">Dim Shook</div>
                    <div className="created-date">3 secs ago</div>
                    <div className="conversation-message">
                        i might need an iFryer
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Stacey Wilson" />
                    <div className="title-text">Bro Hidin</div>
                    <div className="created-date">30 mins ago</div>
                    <div className="conversation-message">
                        Umm...what?
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Stan George" />
                    <div className="title-text">Chef Pesos</div>
                    <div className="created-date">1 week ago</div>
                    <div className="conversation-message">
                        I want my yacht back
                    </div>
                </div>
                <div className="conversation">
                    <img src={require("../../images/blank.jpeg")} alt="Sarah Momes" />
                    <div className="title-text">Sarah Momes</div>
                    <div className="created-date">1 year ago</div>
                    <div className="conversation-message">
                        Thank you. I appreciate that.
                    </div>
                </div>
        </div>
    );
}

export default ConversationList;