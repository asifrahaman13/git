"use client";
import React, { useEffect, useState } from "react";
import { Fragment } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";
import { RespositoryTypes } from "../Types/Repository_types";
import { classNames } from "@/static/Design";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/lib/store";
import { setXmlDataFormat } from "@/lib/features/repository/repositorySlice";
import { fetchDependencies } from "../apis/repository/repository";
import { fetchRepositoriesFromBackend } from "../apis/repository/repository";
import { RepositoryListProps } from "../Types/Repository_types";

const RepositoryList: React.FC<RepositoryListProps> = ({ repositories, selected, setSelected }) => {
  return (
    <>
      <Listbox value={selected} onChange={setSelected}>
        {({ open }) => (
          <>
            <Listbox.Label className="block text-sm font-medium leading-6 text-gray-900">Assigned to</Listbox.Label>
            <div className="relative mt-2">
              <Listbox.Button className="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-600 sm:text-sm sm:leading-6">
                <span className="block truncate">{selected.name}</span>
                <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                  <ChevronUpDownIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
              </Listbox.Button>

              <Transition show={open} as={Fragment} leave="transition ease-in duration-100" leaveFrom="opacity-100" leaveTo="opacity-0">
                <Listbox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                  {repositories.map((repository) => (
                    <Listbox.Option
                      key={repository?.id}
                      className={({ active }) => classNames(active ? "bg-yellow-600 text-white" : "text-gray-900", "relative cursor-default select-none py-2 pl-3 pr-9")}
                      value={repository}
                    >
                      {({ selected, active }) => (
                        <>
                          <span className={classNames(selected ? "font-semibold" : "font-normal", "block truncate")}>{repository?.full_name}</span>

                          {selected ? (
                            <span className={classNames(active ? "text-white" : "text-yellow-600", "absolute inset-y-0 right-0 flex items-center pr-4")}>
                              <CheckIcon className="h-5 w-5" aria-hidden="true" />
                            </span>
                          ) : null}
                        </>
                      )}
                    </Listbox.Option>
                  ))}
                </Listbox.Options>
              </Transition>
            </div>
          </>
        )}
      </Listbox>
    </>
  );
};

const Welcome = () => {
  const dispatch = useDispatch();
  const repository = useSelector((state: RootState) => state.repository);
  const [accessToken, setAccessToken] = useState<string | null>("");
  const [repositories, setRepositories] = useState<RespositoryTypes[]>([]);
  const [selected, setSelected] = useState({ id: 1, name: "Please select one repository" });
  const [msg, setMsg] = useState("");
  const [fetchState, setFetchState] = useState("Click here");

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const access_token = urlParams.get("access_token") || "";
    setAccessToken(access_token);

    async function FetchRepositoriesFromBackend() {
      try {
        const response = await fetchRepositoriesFromBackend(access_token);
        if (response?.status === 200) {
          setRepositories(response.data);
        }
      } catch (error) {
        console.log(error);
      }
    }

    FetchRepositoriesFromBackend();
  }, []);

  async function FetchDependencies() {
    setFetchState("fetching");
    try {
      const response = await fetchDependencies(accessToken, selected.name);
      if (response?.status === 200) {
        if (response.data.status === true) {
          dispatch(setXmlDataFormat({ xmlData: response?.data.xmlData }));
          setMsg("ok");
          setFetchState("fetched");
        } else {
          setMsg("error");
          setFetchState("Something went wrong");
        }
        setTimeout(() => {
          setFetchState("Click here");
        }, 3000);
      } else {
        setMsg("error");
      }
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <>
    
      <div className="w-screen h-screen flex flex-col items-center gap-12 p-32">
        <div className="text-xl font-semibold">Select any of your repository, and hit the button! 🚀</div>
        <div className="w-full xl:w-1/2 flex flex-col gap-4 ">
          <RepositoryList repositories={repositories} selected={selected} setSelected={setSelected} />
          <button
            onClick={(e) => {
              FetchDependencies();
            }}
            className={`${fetchState == "fetching" ? "bg-gray-400" : ""} w-full bg-yellow-500 flex items-center justify-center rounded-xl p-3`}
          >
            {fetchState}
          </button>
        </div>

        <div className="w-full xl:w-1/2">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="sm:flex sm:items-center">
              <div className="sm:flex-auto">
                <h1 className="text-base font-semibold leading-6 text-gray-900">Versions</h1>
                <p className="mt-2 text-sm text-gray-700">A list of all the dependencies and their versions</p>
              </div>
            </div>
            <div className="mt-8 flow-root">
              <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                  <table className="min-w-full divide-y divide-gray-300">
                    <thead>
                      <tr>
                        <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">
                          Name
                        </th>
                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                          Artifact id
                        </th>
                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                          Version
                        </th>
                      </tr>
                    </thead>

                    {msg != "error" && (
                      <tbody className="divide-y divide-gray-200">
                        {repository?.xmlData?.map((person, index) => (
                          <tr key={index}>
                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0">{person.group_id}</td>
                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{person.artifact_id}</td>
                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{person.version}</td>
                          </tr>
                        ))}
                      </tbody>
                    )}
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Welcome;
