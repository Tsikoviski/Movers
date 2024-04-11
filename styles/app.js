// App.js

import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import HomeScreen from './screens/HomeScreen';
import InventoryScreen from './screens/InventoryScreen';
import MovingTipsScreen from './screens/MovingTipsScreen';
import MovingServicesScreen from './screens/MovingServicesScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Inventory" component={InventoryScreen} />
        <Stack.Screen name="MovingTips" component={MovingTipsScreen} />
        <Stack.Screen name="MovingServices" component={MovingServicesScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

