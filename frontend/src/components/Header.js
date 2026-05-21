const Header = ({ title, subtitle }) => {
  return (
    <div className="header">
      <h1 className="text-2xl font-medium tracking-tight" style={{ fontFamily: 'Outfit, sans-serif', color: '#0A0A0A' }}>
        {title}
      </h1>
      {subtitle && (
        <p className="text-sm mt-1" style={{ color: '#52525B' }}>
          {subtitle}
        </p>
      )}
    </div>
  );
};

export default Header;