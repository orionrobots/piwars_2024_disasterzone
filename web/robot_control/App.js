import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { KorolJoystick } from "korol-joystick";

export default function App() {
  return (
    <GestureHandlerRootView style={styles.container}>
      <Text>Control the robot in GestureHandlerRootView </Text>
      <KorolJoystick color="#06b6d4" radius={75} onMove={onJoystickMove} onStop={onJoyStickStop}></KorolJoystick>
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

// Handlers for joystick
const onJoystickMove = (data) => {
  console.log('Joystick move');
  console.log(data);
}

const onJoyStickStop = () => {
  console.log('Joystick stop');
}
