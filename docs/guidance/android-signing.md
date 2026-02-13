# Android App Signing & Google OAuth Guidance

This document outlines the standards and procedures for managing Android app signing keys and their integration with Google OAuth, specifically for applications deployed via internal private stores.

## 1. Understanding SHA-1 Fingerprints

Google OAuth for Android uses a combination of your **Package Name** (e.g., `com.company.app`) and your signing key's **SHA-1 Fingerprint** to identify your application.

> [!IMPORTANT]
> Google will only authorize OAuth requests (401: invalid_client) if the SHA-1 of the certificate used to sign the running APK matches the SHA-1 registered in the Google Cloud Console.

## 2. Package Naming (Application ID)

The Package Name (or Application ID) uniquely identifies your app on the device and in the Google Cloud Console.

### Permitted Characters & Rules
*   **Characters**: Use lowercase letters (a-z), numbers (0-9), and underscores (_). 
*   **Separators**: Use periods (.) strictly as segment separators.
*   **Constraints**:
    *   Must have at least **two segments** (e.g., `com.example`).
    *   Each segment must start with a letter (not a number or underscore).
    *   Cannot use Java reserved keywords (e.g., `static`, `void`, `case`).
    *   **Case Sensitivity**: Always use **lowercase** to avoid compatibility issues.

### Common Patterns (Reverse Domain Name)
*   **Internal Apps**: `app.10mm.operations.utilisation` (matches deployment domain `10mm.app`)
*   **Project-Specific**: `com.10mm.workshop.monitoring`
*   **Standard**: `com.companyname.appname`

## 3. Debug vs. Release Keys

Android development involves two distinct types of signing keys:

### Debug Key
*   **Purpose**: Local development and testing.
*   **Location**: Typically auto-generated at `~/.android/debug.keystore`.
*   **Behavior**: Most tools (Expo, Android Studio) generate a new one per machine.
*   **Best Practice**: For teams, check the `debug.keystore` into a secure location or shared repository to ensure all developers share the same SHA-1 hash for local OAuth testing.

### Release Key
*   **Purpose**: Production deployments.
*   **Behavior**: Created manually by the developer. This key is the final authority for app updates and production OAuth.
*   **Security**: Must be stored in a secure vault (e.g., Vault, 1Password). If lost, you cannot update your application.

## 3. Deployment Scenarios

### Internal / Private App Stores
When bypassing the public Google Play Store:
1.  **Your Signature is Final**: There is no "Google Play App Signing" middleman.
2.  **Explicit Registration**: You must retrieve the SHA-1 from your production keystore and register it as an "Android" credential in the Google Cloud Console.
3.  **No Client Secret**: Native Android clients do not use a `Client Secret`.

### Google Play Store (Public)
Apps on the public store often use "Google Play App Signing":
1.  You sign with an **Upload Key**.
2.  Google re-signs with a **Production Key**.
3.  You must register **both** the Upload SHA-1 and the Production SHA-1 (found in Play Console > App Integrity) in the Google Cloud Console.

## 4. Useful Commands

### Retrieve Fingerprints

**Via Expo:**
```bash
npx expo fetch:android:hashes
```

**Via Gradle (Native projects):**
```bash
cd android && ./gradlew signingReport
```

**Via Keytool (Directly from file):**
```bash
keytool -list -v -keystore path/to/your.keystore
```

## 5. Summary Table

| Environment | Key | Management | OAuth Requirement |
| :--- | :--- | :--- | :--- |
| **Local Dev** | Debug Keystore | Shared/Local | Register Debug SHA-1 |
| **Private Store** | Production Keystore | Secure Vault | Register Prod SHA-1 |
| **Google Play** | Upload Keystore | Secure Vault | Register Upload & Play SHA-1 |
