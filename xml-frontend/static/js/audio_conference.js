const user_username = JSON.parse(document.getElementById('user_username').textContent);
const room_name = JSON.parse(document.getElementById('room-name').textContent);

const makeAudioCall = () => {
    const roomID = room_name // getUrlParams(window.location.href)['roomID'] || (Math.floor(Math.random() * 10000) + "");
    const userID = Math.floor(Math.random() * 10000) + "";
    const userName = user_username;
    const appID = 695007567;
    const serverSecret = "7cd9c382dfdcd55a6705ff0db7dd02e5";
    const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, roomID, userID, userName);

    
        const zp = ZegoUIKitPrebuilt.create(kitToken);
        zp.joinRoom({
            container: document.querySelector("#root"),
            sharedLinks: [{
                name: 'Personal link',
                url: window.location.protocol + '//' + window.location.host  + window.location.pathname + '?roomID=' + roomID,
            }],
            scenario: {
                mode: ZegoUIKitPrebuilt.VideoConference,
            },
                
           	turnOnMicrophoneWhenJoining: false,
           	turnOnCameraWhenJoining: false,
           	showMyCameraToggleButton: false,
           	showMyMicrophoneToggleButton: true,
           	showAudioVideoSettingsButton: false,
           	showScreenSharingButton: false,
           	showTextChat: true,
           	showUserList: true,
           	maxUsers: 50,
           	layout: "Auto",
           	showLayoutButton: true,
         
            });
}

document.getElementById("call-audio-button").addEventListener("click", () => {
    console.log("audio clicked")
    makeAudioCall()
})