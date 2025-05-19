import axios from 'axios';

export const logoutUser = async () => {
  const token = localStorage.getItem('token');
  const tenant = localStorage.getItem('tenant');
  const hostname = window.location.hostname;

  if (!token || !tenant) {
    alert('Token or tenant missing');
    return;
  }

  const isSubdomain = hostname !== 'localhost' && hostname.split('.').length > 1;

  const apiHost = isSubdomain
    ? `http://${hostname}:8000`                     
    : `http://${tenant}.localhost:8000`;           

  try {
    await axios.post(
      `${apiHost}/logout/`,
      {},
      {
        headers: {
          Authorization: `Token ${token}`,
          'X-Tenant-Schema': tenant,
        },
      }
    );

    localStorage.clear();
    window.location.href = '/';
  } catch (err: any) {
    console.error('Logout error:', err);
    alert(err.response?.data?.detail || 'Logout failed.');
  }
};
