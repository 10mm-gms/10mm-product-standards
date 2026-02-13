import React from 'react';

interface LayoutProps {
    children: React.ReactNode;
    showHeader?: boolean;
    logoUrl?: string;
    logoAlt?: string;
    logoHref?: string;
    navLinks?: Array<{ label: string; href: string }>;
}

export const Layout: React.FC<LayoutProps> = ({
    children,
    showHeader = true,
    logoUrl = "/assets/logo_colour_reverse.svg",
    logoAlt = "Company Logo",
    logoHref = "https://github.com/10mm-gms",
    navLinks = [
        { label: "GitHub", href: "https://github.com/10mm-gms" },
        { label: "Login", href: "/admin/login" }
    ]
}) => {
    return (
        <div className="min-h-screen bg-background font-sans text-foreground">
            {showHeader && (
                <header data-testid="standardized-header" className="bg-white border-b border-gray-200 h-[73px] flex items-center sticky top-0 z-50">
                    <div className="container mx-auto px-4 flex justify-between items-center max-w-[90%] w-full">
                        <a href={logoHref} target="_blank" rel="noopener noreferrer" className="transition-opacity hover:opacity-80">
                            <img src={logoUrl} alt={logoAlt} className="h-10 w-auto" />
                        </a>
                        <nav className="flex items-center gap-6">
                            {navLinks.map((link) => (
                                <a
                                    key={link.href}
                                    href={link.href}
                                    className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
                                >
                                    {link.label}
                                </a>
                            ))}
                        </nav>
                    </div>
                </header>
            )}

            <main>
                {children}
            </main>
        </div>
    );
};
