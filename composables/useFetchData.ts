export const useFetchData = async (path: string): Promise<any> => {
  try {
    const config = useRuntimeConfig();
    const baseURL = config.public.baseURL as string;
    const { data } = await useFetch(path, {
      baseURL,
      method: 'GET',
      cache: 'force-cache',
    });
    return data.value;
  } catch (err) {
    console.log(err);
    console.log(err);
  }
};
export const useFetchData_2 = async (path: string): Promise<any> => {
  try {
    const config = useRuntimeConfig();
    const { data } = await useFetch(path, {
      method: 'GET',
      cache: 'force-cache',
    });
    return data.value;
  } catch (err) {
    console.log(err);
    console.log(err);
  }
};
