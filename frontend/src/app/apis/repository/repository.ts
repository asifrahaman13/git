import axios from "axios";
async function fetchDependencies(accessToken: string | null, repo_name: string) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_BACKEND}/repositories/dependencies`,
      {
        repo_name: repo_name,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );
    return response;
  } catch (error) {
    console.log(error);
  }
}

async function fetchRepositoriesFromBackend (accessToken:string, ) {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/repositories/repositories`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
     return response
    } catch (error) {
      console.error("Failed to fetch repositories:", error);
    }
  };

export { fetchDependencies ,fetchRepositoriesFromBackend};
