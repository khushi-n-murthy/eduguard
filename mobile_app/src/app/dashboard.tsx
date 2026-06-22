import { useEffect, useState } from 'react';
import { ActivityIndicator, SafeAreaView, StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { MaxContentWidth, Spacing } from '@/constants/theme';

type DashboardStats = {
  total: number;
  low: number;
  medium: number;
  high: number;
};

export default function DashboardScreen() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const url = 'http://13.201.52.51:8000/dashboard/stats';

    fetch(url)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Server returned ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setStats(data);
        setError(null);
      })
      .catch((err) => {
        setError(
          'Unable to load dashboard data. Make sure the backend is running at http://13.201.52.51:8000',
        );
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <ThemedText type="title" style={styles.title}>
          Teacher Dashboard
        </ThemedText>

        <ThemedView style={styles.card}>
          <ThemedText type="subtitle">Student Performance Summary</ThemedText>
          {loading ? (
            <ActivityIndicator size="large" />
          ) : error ? (
            <ThemedText type="default" style={styles.error}>
              {error}
            </ThemedText>
          ) : stats ? (
            <View style={styles.statsGrid}>
              <View style={styles.statItem}>
                <ThemedText type="subtitle">Total</ThemedText>
                <ThemedText type="default" style={styles.statValue}>
                  {stats.total}
                </ThemedText>
              </View>
              <View style={styles.statItem}>
                <ThemedText type="subtitle">Low Risk</ThemedText>
                <ThemedText type="default" style={styles.statValue}>
                  {stats.low}
                </ThemedText>
              </View>
              <View style={styles.statItem}>
                <ThemedText type="subtitle">Medium Risk</ThemedText>
                <ThemedText type="default" style={styles.statValue}>
                  {stats.medium}
                </ThemedText>
              </View>
              <View style={styles.statItem}>
                <ThemedText type="subtitle">High Risk</ThemedText>
                <ThemedText type="default" style={styles.statValue}>
                  {stats.high}
                </ThemedText>
              </View>
            </View>
          ) : null}
        </ThemedView>

        <ThemedView style={styles.noteBox}>
          <ThemedText type="smallBold">Note</ThemedText>
          <ThemedText type="small">
            This dashboard retrieves live risk categories from the backend.
          </ThemedText>
          <ThemedText type="small">
            If loading fails, verify the API is running and accessible.
          </ThemedText>
        </ThemedView>
      </SafeAreaView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  safeArea: {
    flex: 1,
    width: '100%',
    maxWidth: MaxContentWidth,
    paddingHorizontal: Spacing.four,
    paddingVertical: Spacing.four,
    gap: Spacing.four,
  },
  title: {
    textAlign: 'left',
  },
  card: {
    padding: Spacing.four,
    borderRadius: Spacing.four,
    gap: Spacing.three,
  },
  statsGrid: {
    marginTop: Spacing.three,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: Spacing.three,
  },
  statItem: {
    width: '48%',
    padding: Spacing.three,
    borderRadius: Spacing.three,
    backgroundColor: '#ffffff20',
  },
  statValue: {
    marginTop: Spacing.one,
    fontSize: 32,
  },
  error: {
    color: '#d9534f',
  },
  noteBox: {
    padding: Spacing.three,
    borderRadius: Spacing.three,
    backgroundColor: '#ffffff10',
    gap: Spacing.one,
  },
});
