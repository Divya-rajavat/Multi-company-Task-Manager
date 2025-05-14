import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../Style/Tasks.css';

interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  assigned_to_username: string;
  due_date?: string;
}

interface Theme {
  theme_name: string;
  primary_color: string;
  secondary_color: string;
  background_color: string;
  font_family: string;
}

function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<Theme | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const token = localStorage.getItem('token');
  const tenantDomain = localStorage.getItem('tenant_domain');

  const fetchTasks = async () => {
    try {
      if (!tenantDomain) {
        throw new Error('Tenant domain not found. Please login again.');
      }

      const response = await axios.get(`http://${tenantDomain}:8000/tasks/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      setTasks(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const fetchThemes = async () => {
    try {
      const response = await axios.get(`http://${tenantDomain}:8000/theme/`);
      const allThemes: Theme[] = response.data;

      setThemes(allThemes);

      const savedThemeName = localStorage.getItem('selected_theme');
      const matchingTheme = allThemes.find((t) => t.theme_name === savedThemeName);

      setSelectedTheme(matchingTheme || allThemes[0]);
    } catch (err) {
      console.error('Failed to load themes', err);
    }
  };

  useEffect(() => {
    fetchTasks();
    fetchThemes();
  }, []);

  useEffect(() => {
    if (selectedTheme) {
      localStorage.setItem('selected_theme', selectedTheme.theme_name);
    }
  }, [selectedTheme]);

  const handleCreate = () => {
    navigate('/create-task');
  };

  const themeStyles = selectedTheme
    ? {
        '--primary-color': selectedTheme.primary_color,
        '--secondary-color': selectedTheme.secondary_color,
        '--background-color': selectedTheme.background_color,
        '--font-family': selectedTheme.font_family,
      } as React.CSSProperties
    : {};

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="tasks-container" style={themeStyles}>
      <div className="header">
        <h1>Task List</h1>
        <div className="theme-select">
          <label htmlFor="theme-dropdown">Theme:</label>
          <select
            id="theme-dropdown"
            value={selectedTheme?.theme_name || ''}
            onChange={(e) => {
              const theme = themes.find((t) => t.theme_name === e.target.value);
              if (theme) setSelectedTheme(theme);
            }}
          >
            {themes.length === 0 ? (
              <option disabled>Loading themes...</option>
            ) : (
              themes.map((theme) => (
                <option key={theme.theme_name} value={theme.theme_name}>
                  {theme.theme_name}
                </option>
              ))
            )}
          </select>
        </div>
      </div>

      <ul>
        {tasks.map((task) => (
          <li key={task.id} className="task-card">
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Status: {task.status}</p>
            <p>Assigned To: {task.assigned_to_username}</p>
            {task.due_date && <p>Due Date: {task.due_date}</p>}
          </li>
        ))}
      </ul>

      <button onClick={handleCreate} type="button">
        Create Task
      </button>
    </div>
  );
}

export default Tasks;
