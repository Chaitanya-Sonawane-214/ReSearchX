import { useNavigate } from "react-router-dom";
import { FileQuestion } from "lucide-react";
import { EmptyState } from "../components/ui/EmptyState";
import { Button } from "../components/ui/Button";

export default function NotFound() {
  const navigate = useNavigate();
  return (
    <div className="flex h-full items-center justify-center py-16">
      <EmptyState
        icon={FileQuestion}
        title="Page not found"
        description="The page you're looking for doesn't exist or the paper may have been removed."
        action={<Button onClick={() => navigate("/")}>Back to Dashboard</Button>}
      />
    </div>
  );
}
