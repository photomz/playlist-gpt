const Layout = ({ children }: { children?: React.ReactNode }) => (
  <div className="absolute inset-0 max-h-screen flex flex-col">
    <main className="flex-1 relative overflow-y-scroll overflow-x-hidden bg-teal-100">
      <div className="min-h-full p-0 flex flex-row overflow-x-hidden absolute inset-0 bg-teal-100">
        {children}
      </div>
    </main>
  </div>
);

export default Layout;
