
export enum AppState {
  ONBOARDING = 'ONBOARDING',
  AUTH = 'AUTH',
  HOME = 'HOME',
  REPORT = 'REPORT',
  DASHBOARD = 'DASHBOARD',
  SUCCESS = 'SUCCESS',
  PROFILE = 'PROFILE',
  ISSUE_DETAIL = 'ISSUE_DETAIL'
}

export interface Location {
  latitude: number;
  longitude: number;
  address?: string;
}

export enum IssueStatus {
  SUBMITTED = "submitted",
  CLASSIFIED = "classified",
  ROUTED = "routed",
  VERIFIED = "verified",
  IN_PROGRESS = "in_progress",
  RESOLVED = "resolved",
}

export interface CivicIssue {
  id: string;
  description: string;
  image_url: string;
  location: Location;
  status: IssueStatus;
  created_at?: string;
  category?: string; // Adding optional category since it's used in DashboardScreen
}

export interface User {
  id: string;
  isVerified: boolean;
  name?: string;
  verificationHash: string;
}
