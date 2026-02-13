# 5. Use React Native & Expo for Mobile Applications

Date: 2025-12-21

## Status

Accepted

## Context

We anticipate building mobile applications for several products, including requirements for native hardware access (Camera for condition photos).
We have already selected React for the web frontend (ADR-0003 Context), creating a skill pool in JavaScript/TypeScript/React.
The team needs to support both iOS and Android without maintaining two distinct native codebases (Swift/Kotlin).

## Decision

We will use **React Native** with the **Expo** framework for all mobile applications.

*   **Framework**: **Expo**. We will use the "Managed Workflow" where possible for ease of builds and updates.
*   **Language**: **TypeScript** (Shared with Web).
*   **Styling**: **NativeWind**. Although React Native doesn't use CSS, NativeWind allows us to use the exact same Tailwind classes we use on the web.
*   **Navigation**: **Expo Router** (File-based routing, similar to Next.js on the web).

## Consequences

*   **Positive (Android/iOS Parity)**: React Native renders to true native UI widgets on both platforms. It is not a "webview" wrapper; it feels native because it *is* native.
*   **Positive (Code Reuse)**: We can share extensive logic (state, API clients, validation) between the Web and Mobile repos (or arguably a monorepo).
*   **Positive (Hardware)**: Expo provides robust SDKs for Camera, Location, Notifications, etc., that work identically across both platforms.
*   **Negative**: Some extremely high-performance animations (60fps gestures) require more care than in pure native code, but this is rarely a blocker for business apps like "Vehicle Check."
