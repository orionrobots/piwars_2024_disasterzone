import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { KorolJoystick } from "korol-joystick";

import Paho from "paho-mqtt";

export default function App() {
  
  return (
    <GestureHandlerRootView style={styles.container}>
      <Text>Control the robot!</Text>
      <KorolJoystick color="#06b6d4" radius={75} onMove={onJoystickMove} onStop={onJoyStickStop} />
      <StatusBar style="auto" />
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

var connected = false;
// How to fetch the settings
// https://stackoverflow.com/questions/65903774/receive-mqtt-messages-on-react-native-expo
const mqttClient = new Paho.Client(
  'orionrob-disaster.local',
  Number(9001),
  '/mqtt',
  'robot_control'
);

const reconnect = function(and_do=() => {}) {
  console.log('Connecting to MQTT broker');
  mqttClient.connect({
    userName: 'danny',
    password: 'learnrob3_mqtt',
    keepAliveInterval: 60,
    reconnect: true,
    onSuccess: () => {
      console.log('Connected to MQTT broker');
      connected = true;
      and_do();
    },
    onFailure: (err) => {
      console.log('Connection to MQTT broker failed');
      console.log(err);
      connected = false;
    },
  });
}

reconnect();

mqttClient.onConnectionLost = (err) => {
  console.log('Connection to MQTT broker lost');
  console.log(err);
  connected = false;
};

// Handlers for joystick
const checkConnectionAndSend = (topic, payload) => {
  data = JSON.stringify(payload);
  if (!connected) {
    reconnect(
      () => {
        mqttClient.publish(topic, data);
      }
    );
  } else {
    mqttClient.publish(topic, data);
  }
}

const onJoystickMove = async (data) => {
  // console.log('Joystick move');
  // console.log(data);
  let speed = Math.sin(data.angle.radian) * Math.min(1, data.force);
  let curve = Math.cos(data.angle.radian) * Math.min(1, data.force);
  console.log("speed: " + speed + "\t curve: " + curve);
  checkConnectionAndSend('motors/forward', {speed: speed, curve: curve});
}

const onJoyStickStop = () => {
  console.log('Joystick stop');
  checkConnectionAndSend('motors/stop', {});
}
