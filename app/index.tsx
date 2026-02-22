import { addDays, format, subDays } from "date-fns";
import React, { useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";


type LessonInfos = {
  name: string;
  startTime: string;
  endTime: string;
  site: string[] ;
  room: string[] ;
  type: string;
};

const LessonCell = (props: LessonInfos) => {
  return (
    <View style={styles.lessonCell}>
      <Text>{props.startTime} - {props.endTime}</Text>
      <Text>{props.name}</Text>
    </View>
  );
};

export default function Home() {
  const [currentDate, setCurrentDate] = useState(new Date());

  const scheduleTimes = ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30", "17:00", "18:30", "20:00"];

  const goToPreviousDay = () => setCurrentDate((date) => subDays(date, 1));
  const goToNextDay = () => setCurrentDate((date) => addDays(date, 1));

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={goToPreviousDay} style={styles.arrowButton}>
          <Text style={styles.arrowText}>{"<"}</Text>
        </TouchableOpacity>
        <Text style={styles.dateText}>
          {format(currentDate, "EEEE d MMMM yyyy")}
        </Text>
        <TouchableOpacity onPress={goToNextDay} style={styles.arrowButton}>
          <Text style={styles.arrowText}>{">"}</Text>
        </TouchableOpacity>
      </View>
        <View style={styles.body}>
          <View style={styles.timeZone}>
            {scheduleTimes.map((time) => (
              <View key={time} style={styles.timeCell}>
                <Text>{time}</Text>
              </View>
            ))}
          </View>
          <View style={styles.lessonsZone}>
              {scheduleTimes.map((time) => (
                <View style={styles.lessonCell}>
                </View>
              ))}
          </View>
        </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingTop: 1,
    paddingBottom: 1,
    marginBottom: 1,
    backgroundColor: "#bebbbb",
  },
  body: {
    flex: 1,
    flexDirection: "row",
    paddingHorizontal: 10,
    marginTop: 1,
    backgroundColor: "#6b6b6b",
  },
  // Style for element in the header
  arrowButton: {
    padding: 10,
  },
  arrowText: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#333",
  },
  dateText: {
    fontSize: 20,
    fontWeight: "bold",
    marginHorizontal: 20,
    color: "#333",
  },
  // Style for element in the body
  timeZone: {
    flex: 1,
    flexDirection: "column",
    marginTop: 5,
    marginRight: 5,
    backgroundColor: "#fff",
    alignItems: "center",
    borderRadius: 5,
  },
  lessonsZone: {
    flex: 8,
    flexDirection: "column",
    marginTop: 5,
    marginLeft: 5,
    backgroundColor: "#fff",
    borderRadius: 5,
  },
  timeCell: {
    flex: 1,
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    borderBottomWidth: 1,
    borderBottomColor: "#000000",
  },
  lessonCell: {
    flex: 1,
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    borderBottomWidth: 1,
    borderBottomColor: "#000000",
  },

  
});
