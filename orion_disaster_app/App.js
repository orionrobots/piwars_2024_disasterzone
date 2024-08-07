import Paho from "paho-mqtt";
import { StatusBar } from 'expo-status-bar';
import { Text, View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { ReactNativeJoystick } from "@korsolutions/react-native-joystick";
import { styles } from "./styles";
import * as env from "./env";


export default function App() {
  return (
    <GestureHandlerRootView style={styles.container}>
      <Text>Control the robot!</Text>
      <ReactNativeJoystick color="#06b6d4" radius={75} onMove={onJoystickMove} onStop={onJoyStickStop}/>
      <ReactNativeJoystick color="#06b6d4" radius={75} onMove={onServostickMove} onStop={onServostickStop}/>
      <StatusBar style="auto" />
    </GestureHandlerRootView>
  );
}

const mqttClient = new Paho.Client(
  env.PI_HOSTNAME,
  Number(9001),
  "robot_control"
);

mqttClient.onConnectionLost = (err) => {
  console.log("Connected to MQTT broker lost");
  console.log(err);
};

console.log("Attempting to connect to " + env.PI_HOSTNAME);
mqttClient.connect({
  userName: env.MQTT_USERNAME,
  password: env.MQTT_PASSWORD,
  onSuccess: () => {
    console.log("Connected");
  },
  onFailure: (err) => {
    console.log('Connection failed');
    console.log(err)
  },
});

// Handlers for joystick
const onJoystickMove = (data) => {
  // console.log('Joystick move');
  // console.log(data);
  let speed = Math.sin(data.angle.radian) * Math.min(1, data.force);
  let curve = Math.cos(data.angle.radian) * Math.min(1, data.force);
  console.log("speed: "+speed+"\t curve: "+curve);
  data = JSON.stringify({speed: speed, curve: -curve});
  mqttClient.publish("motors/forward", data);
};

const onJoyStickStop = () => {
  // console.log('Joystick stop');
  mqttClient.publish("motors/stop", "{}");
};


// Handlers for servos
const onServostickMove = (data) => {
  // console.log('Joystick move');
  // console.log(data);
  let tilt = Math.sin(data.angle.radian) * Math.min(1, data.force) * 50;
  let pan = Math.cos(data.angle.radian) * Math.min(1, data.force) * -80;
  console.log("tilt: "+tilt+"\t pan: "+pan);
  mqttClient.publish("servos/set", JSON.stringify({"index": 0, "position": pan}));
  mqttClient.publish("servos/set", JSON.stringify({"index": 1, "position": tilt}));
};

const onServostickStop = () => {
  // console.log('Joystick stop');
  mqttClient.publish("servos/stop", JSON.stringify({"index": 0}));
};
